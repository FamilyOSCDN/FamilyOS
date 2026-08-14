"""Tests for application-owned Python package structural validation."""

from __future__ import annotations

import gzip
import io
import stat
import struct
import tarfile
import zipfile
from pathlib import Path
from types import TracebackType
from typing import BinaryIO

import pytest

import familyos_cli.application.build.validate_python_package_artifacts as validation_module
from familyos_cli.application.build import (
    ArtifactClass,
    DiscoveredArtifact,
    PackageStructuralValidationStatus,
    ValidatePythonPackageArtifactsUseCase,
)

PACKAGE_NAME = "familyos-cli"
ARCHIVE_NAME = "familyos_cli"
PACKAGE_VERSION = "0.1.0"


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "{PACKAGE_NAME}"\nversion = "{PACKAGE_VERSION}"\n',
        encoding="utf-8",
    )
    return root


def _core_metadata(
    *,
    name: str = PACKAGE_NAME,
    version: str = PACKAGE_VERSION,
) -> str:
    return f"Metadata-Version: 2.4\nName: {name}\nVersion: {version}\n\n"


def _wheel_metadata() -> str:
    return (
        "Wheel-Version: 1.0\n"
        "Generator: FamilyOS tests\n"
        "Root-Is-Purelib: true\n"
        "Tag: py3-none-any\n"
        "\n"
    )


def _write_wheel(
    path: Path,
    *,
    metadata: str | None = None,
    wheel_metadata: str | None = None,
    record: str | None = None,
    omitted: tuple[str, ...] = (),
    extra_members: tuple[tuple[str, str | bytes], ...] = (),
) -> None:
    dist_info = f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.dist-info"
    members: dict[str, str | bytes] = {
        f"{ARCHIVE_NAME}/__init__.py": "",
        f"{dist_info}/METADATA": metadata or _core_metadata(),
        f"{dist_info}/WHEEL": wheel_metadata or _wheel_metadata(),
    }
    members.update(dict(extra_members))
    members = {
        name: content
        for name, content in members.items()
        if name.rsplit("/", 1)[-1] not in omitted
    }
    record_path = f"{dist_info}/RECORD"
    if "RECORD" not in omitted:
        record_names = (*members, record_path)
        members[record_path] = record or "".join(f"{name},,\n" for name in record_names)
    with zipfile.ZipFile(
        path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for name, content in members.items():
            archive.writestr(name, content)


def _add_tar_text(archive: tarfile.TarFile, name: str, content: str) -> None:
    _add_tar_bytes(archive, name, content.encode())


def _add_tar_bytes(archive: tarfile.TarFile, name: str, content: bytes) -> None:
    member = tarfile.TarInfo(name)
    member.size = len(content)
    archive.addfile(member, io.BytesIO(content))


def _write_sdist(
    path: Path,
    *,
    metadata: str | None = None,
    root: str = f"{ARCHIVE_NAME}-{PACKAGE_VERSION}",
    extra_members: tuple[tuple[str, str | bytes], ...] = (),
) -> None:
    with tarfile.open(path, mode="w:gz") as archive:
        _add_tar_text(archive, f"{root}/PKG-INFO", metadata or _core_metadata())
        _add_tar_text(
            archive,
            f"{root}/pyproject.toml",
            f'[project]\nname = "{PACKAGE_NAME}"\nversion = "{PACKAGE_VERSION}"\n',
        )
        _add_tar_text(archive, f"{root}/src/{ARCHIVE_NAME}/__init__.py", "")
        for name, content in extra_members:
            _add_tar_bytes(
                archive,
                name,
                content.encode() if isinstance(content, str) else content,
            )


class _TrackingZipStream(io.BytesIO):
    def __init__(self, content: bytes) -> None:
        super().__init__(content)
        self.actual_bytes_returned = 0

    def read(self, size: int | None = -1) -> bytes:
        assert size is not None and size >= 0
        data = super().read(size)
        self.actual_bytes_returned += len(data)
        return data


def _install_synthetic_zip(
    monkeypatch: pytest.MonkeyPatch,
    entries: tuple[tuple[str, int, bytes], ...],
) -> list[_TrackingZipStream]:
    members: list[zipfile.ZipInfo] = []
    content_by_name: dict[str, bytes] = {}
    for name, declared_size, content in entries:
        member = zipfile.ZipInfo(name)
        member.create_system = 3
        member.external_attr = (stat.S_IFREG | 0o644) << 16
        member.compress_type = zipfile.ZIP_DEFLATED
        member.file_size = declared_size
        members.append(member)
        content_by_name[name] = content
    streams: list[_TrackingZipStream] = []

    class _SyntheticZipFile:
        def __init__(self, path: Path, mode: str) -> None:
            assert path.is_file()
            assert mode == "r"

        def __enter__(self) -> _SyntheticZipFile:
            return self

        def __exit__(
            self,
            exception_type: type[BaseException] | None,
            exception: BaseException | None,
            traceback: TracebackType | None,
        ) -> None:
            return None

        def infolist(self) -> list[zipfile.ZipInfo]:
            return members

        def open(
            self,
            member: zipfile.ZipInfo,
            mode: str,
        ) -> _TrackingZipStream:
            assert mode == "r"
            stream = _TrackingZipStream(content_by_name[member.filename])
            streams.append(stream)
            return stream

    monkeypatch.setattr(zipfile, "ZipFile", _SyntheticZipFile)
    return streams


def _forge_central_uncompressed_size(
    path: Path,
    member_name: str,
    declared_size: int,
) -> None:
    archive_bytes = bytearray(path.read_bytes())
    end_record = archive_bytes.rfind(b"PK\x05\x06")
    assert end_record >= 0
    central_size = struct.unpack_from("<I", archive_bytes, end_record + 12)[0]
    central_offset = struct.unpack_from("<I", archive_bytes, end_record + 16)[0]
    position = central_offset
    central_end = central_offset + central_size
    while position < central_end:
        assert archive_bytes[position : position + 4] == b"PK\x01\x02"
        name_length, extra_length, comment_length = struct.unpack_from(
            "<HHH",
            archive_bytes,
            position + 28,
        )
        name_start = position + 46
        name_end = name_start + name_length
        name = archive_bytes[name_start:name_end].decode()
        if name == member_name:
            struct.pack_into("<I", archive_bytes, position + 24, declared_size)
            path.write_bytes(archive_bytes)
            return
        position = name_end + extra_length + comment_length
    raise AssertionError(f"central member {member_name!r} not found")


def _candidate(path: Path, artifact_class: ArtifactClass) -> DiscoveredArtifact:
    return DiscoveredArtifact(path=path, artifact_class=artifact_class)


def test_valid_wheel_is_structurally_valid(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel)

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.VALID
    assert result.diagnostic is None
    assert result.candidate_results[0].diagnostics == ()
    assert result.candidate_results[0].candidate.path == wheel
    for field in (
        "trusted",
        "verified",
        "release_ready",
        "digest",
        "build_id",
        "provenance",
    ):
        assert not hasattr(result, field)


def test_wheel_directory_entries_remain_structurally_valid(
    project_root: Path,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    dist_info = f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.dist-info"
    _write_wheel(
        wheel,
        extra_members=((f"{ARCHIVE_NAME}/", ""), (f"{dist_info}/", "")),
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.VALID
    assert result.diagnostic is None


def test_corrupt_wheel_is_invalid(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    wheel.write_bytes(b"not a ZIP archive")

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert wheel.name in result.diagnostic
    assert "unreadable or corrupt" in result.diagnostic


@pytest.mark.parametrize("missing", ["METADATA", "WHEEL", "RECORD"])
def test_missing_required_wheel_metadata_is_invalid(
    project_root: Path,
    missing: str,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel, omitted=(missing,))

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert f"missing required {missing}" in result.diagnostic


def test_malformed_wheel_core_metadata_is_invalid(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(
        wheel,
        metadata="Metadata-Version: 2.4\nMalformed core metadata\n",
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "wheel METADATA is malformed" in result.diagnostic


def test_malformed_wheel_metadata_is_invalid(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(
        wheel,
        wheel_metadata=(
            "Wheel-Version: invalid\nRoot-Is-Purelib: sometimes\nTag: malformed\n\n"
        ),
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "malformed Wheel-Version" in result.diagnostic
    assert "malformed Root-Is-Purelib" in result.diagnostic
    assert "malformed Tag" in result.diagnostic


def test_incoherent_wheel_identity_is_invalid(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel, metadata=_core_metadata(version="9.9.9"))

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "name/version does not match" in result.diagnostic


def test_wheel_with_traversal_member_is_invalid_without_extraction(
    project_root: Path,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel, extra_members=(("../outside.py", "malicious"),))

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "unsafe path" in result.diagnostic
    assert not (project_root.parent / "outside.py").exists()


@pytest.mark.parametrize(
    "member_type",
    [stat.S_IFLNK, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFIFO, stat.S_IFSOCK],
)
def test_wheel_rejects_unsupported_unix_member_types(
    project_root: Path,
    member_type: int,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel)
    special_member = zipfile.ZipInfo(f"{ARCHIVE_NAME}/special")
    special_member.create_system = 3
    special_member.external_attr = (member_type | 0o777) << 16
    special_member.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(wheel, mode="a") as archive:
        archive.writestr(special_member, b"target")

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "unsupported non-regular Unix file type" in result.diagnostic


def test_wheel_rejects_malformed_record_csv(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel, record='"unterminated,,\n')

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "RECORD is malformed CSV" in result.diagnostic


def test_wheel_rejects_duplicate_normalized_member_paths(
    project_root: Path,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(
        wheel,
        extra_members=(("collision", "file"), ("collision/", "")),
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "duplicate normalized member path 'collision'" in result.diagnostic


def test_forged_wheel_size_is_bounded_by_actual_streamed_bytes(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    wheel.touch()
    dist_info = f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.dist-info"
    hostile_payload = b"x" * 4096
    streams = _install_synthetic_zip(
        monkeypatch,
        (
            (f"{ARCHIVE_NAME}/payload.py", 1, hostile_payload),
            (f"{dist_info}/METADATA", 1, _core_metadata().encode()),
            (f"{dist_info}/WHEEL", 1, _wheel_metadata().encode()),
            (f"{dist_info}/RECORD", 1, b"placeholder,,\n"),
        ),
    )
    monkeypatch.setattr(validation_module, "_STREAM_CHUNK_BYTES", 64)
    monkeypatch.setattr(
        validation_module,
        "_WHEEL_MEMBER_ACTUAL_BYTES_LIMIT",
        256,
    )
    monkeypatch.setattr(
        validation_module,
        "_WHEEL_AGGREGATE_ACTUAL_BYTES_LIMIT",
        8192,
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "actual decompressed content exceeds per-member" in result.diagnostic
    assert sum(stream.actual_bytes_returned for stream in streams) == 257
    assert sum(stream.actual_bytes_returned for stream in streams) < len(
        hostile_payload
    )


def test_wheel_actual_aggregate_bound_stops_streaming(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    wheel.touch()
    dist_info = f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.dist-info"
    streams = _install_synthetic_zip(
        monkeypatch,
        (
            (f"{ARCHIVE_NAME}/first.py", 1, b"a" * 200),
            (f"{ARCHIVE_NAME}/second.py", 1, b"b" * 200),
            (f"{dist_info}/METADATA", 1, _core_metadata().encode()),
            (f"{dist_info}/WHEEL", 1, _wheel_metadata().encode()),
            (f"{dist_info}/RECORD", 1, b"placeholder,,\n"),
        ),
    )
    monkeypatch.setattr(validation_module, "_STREAM_CHUNK_BYTES", 64)
    monkeypatch.setattr(
        validation_module,
        "_WHEEL_MEMBER_ACTUAL_BYTES_LIMIT",
        256,
    )
    monkeypatch.setattr(
        validation_module,
        "_WHEEL_AGGREGATE_ACTUAL_BYTES_LIMIT",
        300,
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "actual decompressed content exceeds aggregate" in result.diagnostic
    assert sum(stream.actual_bytes_returned for stream in streams) == 301


def test_wheel_rejects_oversized_declared_member_before_streaming(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(
        wheel,
        extra_members=((f"{ARCHIVE_NAME}/oversized.py", b"x" * 1024),),
    )
    monkeypatch.setattr(
        validation_module,
        "_WHEEL_MEMBER_ACTUAL_BYTES_LIMIT",
        512,
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "declared size exceeds per-member" in result.diagnostic


def test_forged_lzma_wheel_is_rejected_before_decompression(
    project_root: Path,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel)
    hostile_member_name = f"{ARCHIVE_NAME}/hostile.py"
    hostile_member = zipfile.ZipInfo(hostile_member_name)
    hostile_member.create_system = 3
    hostile_member.external_attr = (stat.S_IFREG | 0o644) << 16
    hostile_member.compress_type = zipfile.ZIP_LZMA
    with zipfile.ZipFile(wheel, mode="a") as archive:
        archive.writestr(hostile_member, b"x" * 2_000_000)
    _forge_central_uncompressed_size(wheel, hostile_member_name, 1)
    with zipfile.ZipFile(wheel, mode="r") as archive:
        forged_member = archive.getinfo(hostile_member_name)
        assert forged_member.file_size == 1
        assert forged_member.compress_type == zipfile.ZIP_LZMA

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "uses unsupported compression" in result.diagnostic


def test_wheel_member_count_bound_is_enforced(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    _write_wheel(wheel)
    monkeypatch.setattr(validation_module, "_ARCHIVE_MEMBER_COUNT_LIMIT", 3)

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "3-member inspection limit" in result.diagnostic


def test_valid_sdist_is_structurally_valid(project_root: Path) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    _write_sdist(sdist)

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.VALID
    assert result.diagnostic is None


def test_corrupt_sdist_is_invalid(project_root: Path) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    sdist.write_bytes(b"not a gzip-compressed tar archive")

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert sdist.name in result.diagnostic
    assert "unreadable or corrupt" in result.diagnostic


def test_sdist_with_multiple_roots_is_invalid(project_root: Path) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    _write_sdist(sdist, extra_members=(("another-root/file.py", ""),))

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "must contain one package root" in result.diagnostic


def test_incoherent_sdist_metadata_is_invalid(project_root: Path) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    _write_sdist(sdist, metadata=_core_metadata(name="another-package"))

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "name/version does not match" in result.diagnostic


def test_sdist_with_traversal_member_is_invalid_without_extraction(
    project_root: Path,
) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    _write_sdist(sdist, extra_members=(("../outside.py", "malicious"),))

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "unsafe path" in result.diagnostic
    assert not (project_root.parent / "outside.py").exists()


def test_sdist_member_actual_byte_bound_stops_streaming(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    root = f"{ARCHIVE_NAME}-{PACKAGE_VERSION}"
    hostile_payload = b"x" * 4096
    _write_sdist(
        sdist,
        extra_members=((f"{root}/src/{ARCHIVE_NAME}/hostile.py", hostile_payload),),
    )
    decompressed_size = len(gzip.decompress(sdist.read_bytes()))
    readers: list[validation_module._ActualByteLimitReader] = []

    class _TrackingActualByteLimitReader(validation_module._ActualByteLimitReader):
        def __init__(self, stream: BinaryIO, limit: int, diagnostic: str) -> None:
            super().__init__(stream, limit, diagnostic)
            readers.append(self)

    monkeypatch.setattr(
        validation_module,
        "_ActualByteLimitReader",
        _TrackingActualByteLimitReader,
    )
    monkeypatch.setattr(validation_module, "_STREAM_CHUNK_BYTES", 32)
    monkeypatch.setattr(
        validation_module,
        "_SDIST_MEMBER_ACTUAL_BYTES_LIMIT",
        128,
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "actual content exceeds per-member" in result.diagnostic
    assert len(readers) == 1
    assert readers[0].actual_bytes_read < decompressed_size


def test_sdist_actual_aggregate_bound_stops_streaming(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    _write_sdist(sdist)
    monkeypatch.setattr(validation_module, "_STREAM_CHUNK_BYTES", 64)
    monkeypatch.setattr(
        validation_module,
        "_SDIST_AGGREGATE_ACTUAL_BYTES_LIMIT",
        256,
    )

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "actual decompressed content exceeds aggregate" in result.diagnostic


def test_sdist_member_count_bound_is_enforced_during_streaming(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    _write_sdist(sdist)
    monkeypatch.setattr(validation_module, "_ARCHIVE_MEMBER_COUNT_LIMIT", 2)

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "2-member inspection limit" in result.diagnostic


def test_diagnostics_are_candidate_specific_and_deterministic(
    project_root: Path,
) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"
    sdist = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}.tar.gz"
    wheel.write_bytes(b"bad wheel")
    sdist.write_bytes(b"bad sdist")
    validator = ValidatePythonPackageArtifactsUseCase(project_root)
    candidates = (
        _candidate(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
        _candidate(wheel, ArtifactClass.PYTHON_WHEEL),
    )

    first = validator.execute(candidates)
    second = validator.execute(tuple(reversed(candidates)))

    assert first == second
    assert first.diagnostic is not None
    assert first.diagnostic.index(wheel.name) < first.diagnostic.index(sdist.name)
    assert "python-wheel" in first.diagnostic
    assert "source-distribution" in first.diagnostic


def test_missing_candidate_regular_file_is_invalid(project_root: Path) -> None:
    wheel = project_root / f"{ARCHIVE_NAME}-{PACKAGE_VERSION}-py3-none-any.whl"

    result = ValidatePythonPackageArtifactsUseCase(project_root).execute(
        (_candidate(wheel, ArtifactClass.PYTHON_WHEEL),)
    )

    assert result.status is PackageStructuralValidationStatus.INVALID
    assert result.diagnostic is not None
    assert "does not exist as a regular file" in result.diagnostic
