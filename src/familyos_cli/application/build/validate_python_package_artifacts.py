"""Application-owned structural validation for discovered Python packages."""

from __future__ import annotations

import csv
import gzip
import io
import re
import stat
import tarfile
import tomllib
import zipfile
import zlib
from collections import Counter
from dataclasses import dataclass
from email.message import Message
from email.parser import Parser
from email.policy import default
from pathlib import Path, PurePosixPath
from typing import BinaryIO, cast

from familyos_cli.application.build.artifact_discovery import (
    ArtifactClass,
    DiscoveredArtifact,
)
from familyos_cli.application.build.package_validation import (
    CandidatePackageValidationResult,
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
)

# Private bounded-inspection controls for this validator. They reduce resource
# exposure during structural inspection; they are not a universal anti-DoS
# sandbox for hostile archives.
_STREAM_CHUNK_BYTES = 65_536
_ARCHIVE_MEMBER_COUNT_LIMIT = 10_000
_WHEEL_MEMBER_ACTUAL_BYTES_LIMIT = 67_108_864  # 64 MiB
_WHEEL_AGGREGATE_ACTUAL_BYTES_LIMIT = 536_870_912  # 512 MiB
_SDIST_MEMBER_ACTUAL_BYTES_LIMIT = 67_108_864  # 64 MiB
_SDIST_AGGREGATE_ACTUAL_BYTES_LIMIT = 536_870_912  # 512 MiB
_CORE_METADATA_BYTES_LIMIT = 1_048_576  # 1 MiB
_RECORD_BYTES_LIMIT = 16_777_216  # 16 MiB
# ZipExtFile bounds output for stored/deflated entries. Its BZIP2/LZMA readers
# can expand a compressed input chunk without an output limit, so reject those
# methods before opening a member and relying on actual returned-byte counters.
_SUPPORTED_WHEEL_COMPRESSION = frozenset({zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED})
_METADATA_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+$")
_WHEEL_TAG_COMPONENT_PATTERN = re.compile(r"^[A-Za-z0-9_.]+$")


@dataclass(frozen=True, slots=True)
class _PackageNameVersion:
    name: str
    version: str


@dataclass(frozen=True, slots=True)
class _CandidateInspection:
    candidate: DiscoveredArtifact
    identity: _PackageNameVersion | None
    diagnostics: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _SdistStreamInspection:
    roots: frozenset[str]
    regular_member_names: frozenset[str]
    captured_members: dict[str, bytes]
    has_python_source: bool


class _StructuralInspectionLimitExceeded(Exception):
    """Stop archive consumption immediately after an actual-byte limit."""


class _ActualByteLimitReader:
    """Bound actual bytes returned by a decompression stream."""

    def __init__(self, stream: BinaryIO, limit: int, diagnostic: str) -> None:
        self._stream = stream
        self._limit = limit
        self._diagnostic = diagnostic
        self.actual_bytes_read = 0

    def read(self, size: int = -1) -> bytes:
        """Read at most one byte beyond the limit, then stop deterministically."""

        remaining = self._limit - self.actual_bytes_read
        requested = min(
            _STREAM_CHUNK_BYTES if size < 0 else size,
            remaining + 1,
        )
        data = self._stream.read(requested)
        self.actual_bytes_read += len(data)
        if self.actual_bytes_read > self._limit:
            raise _StructuralInspectionLimitExceeded(self._diagnostic)
        return data


class ValidatePythonPackageArtifactsUseCase:
    """Validate exact discovered candidates without rediscovering outputs."""

    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root

    def execute(
        self,
        candidates: tuple[DiscoveredArtifact, ...],
    ) -> PythonPackageStructuralValidationResult:
        """Inspect wheel and sdist streams without filesystem extraction."""

        expected, authority_diagnostic = self._load_project_identity()
        ordered_candidates = tuple(
            sorted(
                candidates,
                key=lambda candidate: (
                    candidate.artifact_class.value,
                    candidate.path.name,
                ),
            )
        )
        inspections = [
            self._inspect_candidate(candidate, expected, authority_diagnostic)
            for candidate in ordered_candidates
        ]
        inspections = self._add_cross_artifact_findings(inspections)
        candidate_results = tuple(
            CandidatePackageValidationResult(
                candidate=inspection.candidate,
                status=(
                    PackageStructuralValidationStatus.INVALID
                    if inspection.diagnostics
                    else PackageStructuralValidationStatus.VALID
                ),
                diagnostics=inspection.diagnostics,
            )
            for inspection in inspections
        )
        return PythonPackageStructuralValidationResult(
            status=(
                PackageStructuralValidationStatus.VALID
                if all(result.successful for result in candidate_results)
                else PackageStructuralValidationStatus.INVALID
            ),
            candidate_results=candidate_results,
        )

    def _load_project_identity(
        self,
    ) -> tuple[_PackageNameVersion | None, str | None]:
        pyproject_path = self._project_root / "pyproject.toml"
        try:
            pyproject_text = pyproject_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return None, "authoritative pyproject.toml is unreadable"
        try:
            return self._parse_pyproject_identity(pyproject_text), None
        except tomllib.TOMLDecodeError:
            return None, "authoritative pyproject.toml is malformed"
        except ValueError as error:
            return None, str(error)

    def _inspect_candidate(
        self,
        candidate: DiscoveredArtifact,
        expected: _PackageNameVersion | None,
        authority_diagnostic: str | None,
    ) -> _CandidateInspection:
        if authority_diagnostic is not None:
            return _CandidateInspection(
                candidate=candidate,
                identity=None,
                diagnostics=(authority_diagnostic,),
            )
        if not candidate.path.is_file() or candidate.path.is_symlink():
            return _CandidateInspection(
                candidate=candidate,
                identity=None,
                diagnostics=("candidate does not exist as a regular file",),
            )
        if candidate.artifact_class is ArtifactClass.PYTHON_WHEEL:
            return self._inspect_wheel(candidate, expected)
        if candidate.artifact_class is ArtifactClass.SOURCE_DISTRIBUTION:
            return self._inspect_sdist(candidate, expected)
        return _CandidateInspection(
            candidate=candidate,
            identity=None,
            diagnostics=(
                f"unsupported artifact class {candidate.artifact_class.value}",
            ),
        )

    def _inspect_wheel(
        self,
        candidate: DiscoveredArtifact,
        expected: _PackageNameVersion | None,
    ) -> _CandidateInspection:
        diagnostics: list[str] = []
        filename_identity = self._parse_wheel_filename(
            candidate.path.name,
            diagnostics,
        )
        metadata_identity: _PackageNameVersion | None = None
        try:
            with zipfile.ZipFile(candidate.path, mode="r") as archive:
                members = archive.infolist()
                members_are_safe = self._validate_zip_members(members, diagnostics)
                dist_info_root = (
                    self._wheel_dist_info_root(members, diagnostics)
                    if members_are_safe
                    else None
                )
                if dist_info_root is not None:
                    required = self._required_wheel_members(dist_info_root)
                    captured_members = self._stream_zip_members(
                        archive,
                        members,
                        {
                            required["METADATA"]: _CORE_METADATA_BYTES_LIMIT,
                            required["WHEEL"]: _CORE_METADATA_BYTES_LIMIT,
                            required["RECORD"]: _RECORD_BYTES_LIMIT,
                        },
                        diagnostics,
                    )
                else:
                    captured_members = None
                if dist_info_root is not None and captured_members is not None:
                    metadata_identity = self._validate_wheel_metadata(
                        members,
                        dist_info_root,
                        captured_members,
                        diagnostics,
                    )
                    self._compare_dist_info_identity(
                        dist_info_root,
                        metadata_identity,
                        diagnostics,
                    )
        except (
            OSError,
            EOFError,
            RuntimeError,
            zipfile.BadZipFile,
            zipfile.LargeZipFile,
            zlib.error,
        ):
            diagnostics.append("wheel archive is unreadable or corrupt")

        identity = metadata_identity or filename_identity
        self._compare_identities(
            "wheel filename",
            filename_identity,
            "wheel package metadata",
            metadata_identity,
            diagnostics,
        )
        self._compare_expected_identity(identity, expected, diagnostics)
        return _CandidateInspection(candidate, identity, tuple(diagnostics))

    def _inspect_sdist(
        self,
        candidate: DiscoveredArtifact,
        expected: _PackageNameVersion | None,
    ) -> _CandidateInspection:
        diagnostics: list[str] = []
        filename_identity = self._parse_sdist_filename(
            candidate.path.name,
            diagnostics,
        )
        metadata_identity: _PackageNameVersion | None = None
        source_identity: _PackageNameVersion | None = None
        try:
            stream_inspection = self._stream_sdist_archive(
                candidate.path,
                diagnostics,
            )
            if stream_inspection is not None:
                package_root = self._sdist_package_root(
                    stream_inspection.roots,
                    diagnostics,
                )
                if package_root is not None:
                    metadata_identity, source_identity = self._validate_sdist_content(
                        stream_inspection,
                        package_root,
                        diagnostics,
                    )
                    self._compare_sdist_root_identity(
                        package_root,
                        metadata_identity,
                        diagnostics,
                    )
        except _StructuralInspectionLimitExceeded as error:
            diagnostics.append(str(error))
        except (OSError, EOFError, tarfile.TarError):
            diagnostics.append("source archive is unreadable or corrupt")

        identity = metadata_identity or source_identity or filename_identity
        self._compare_identities(
            "source-distribution filename",
            filename_identity,
            "source-distribution package metadata",
            metadata_identity,
            diagnostics,
        )
        self._compare_identities(
            "source-distribution package metadata",
            metadata_identity,
            "archived pyproject.toml",
            source_identity,
            diagnostics,
        )
        self._compare_expected_identity(identity, expected, diagnostics)
        return _CandidateInspection(candidate, identity, tuple(diagnostics))

    def _validate_zip_members(
        self,
        members: list[zipfile.ZipInfo],
        diagnostics: list[str],
    ) -> bool:
        valid = True
        if len(members) > _ARCHIVE_MEMBER_COUNT_LIMIT:
            diagnostics.append(
                "wheel archive exceeds "
                f"{_ARCHIVE_MEMBER_COUNT_LIMIT}-member inspection limit"
            )
            return False

        normalized_names = [
            self._normalized_archive_member_name(member.filename) for member in members
        ]
        duplicate_names = sorted(
            name for name, count in Counter(normalized_names).items() if count > 1
        )
        for name in duplicate_names:
            diagnostics.append(
                f"wheel contains duplicate normalized member path {name!r}"
            )
            valid = False

        declared_total = 0
        for member in members:
            path_diagnostic = self._archive_path_diagnostic(member.filename)
            if path_diagnostic is not None:
                diagnostics.append(
                    f"wheel member {member.filename!r} has unsafe path: "
                    f"{path_diagnostic}"
                )
                valid = False
            type_diagnostic = self._zip_member_type_diagnostic(member)
            if type_diagnostic is not None:
                diagnostics.append(
                    f"wheel member {member.filename!r} {type_diagnostic}"
                )
                valid = False
            if member.compress_type not in _SUPPORTED_WHEEL_COMPRESSION:
                diagnostics.append(
                    f"wheel member {member.filename!r} uses unsupported compression"
                )
                valid = False
            if member.file_size < 0:
                diagnostics.append(
                    f"wheel member {member.filename!r} has invalid declared size"
                )
                valid = False
            elif member.file_size > _WHEEL_MEMBER_ACTUAL_BYTES_LIMIT:
                diagnostics.append(
                    f"wheel member {member.filename!r} declared size exceeds "
                    "per-member inspection limit"
                )
                valid = False
            declared_total += max(member.file_size, 0)
        if declared_total > _WHEEL_AGGREGATE_ACTUAL_BYTES_LIMIT:
            diagnostics.append(
                "wheel declared uncompressed content exceeds aggregate inspection limit"
            )
            valid = False
        return valid

    def _zip_member_type_diagnostic(
        self,
        member: zipfile.ZipInfo,
    ) -> str | None:
        if member.create_system != 3:
            return None
        unix_mode = (member.external_attr >> 16) & 0xFFFF
        member_type = stat.S_IFMT(unix_mode)
        if member.is_dir():
            if member_type not in {0, stat.S_IFDIR}:
                return "has unsupported non-directory Unix file type"
            return None
        if member_type not in {0, stat.S_IFREG}:
            return "has unsupported non-regular Unix file type"
        return None

    def _stream_zip_members(
        self,
        archive: zipfile.ZipFile,
        members: list[zipfile.ZipInfo],
        capture_limits: dict[str, int],
        diagnostics: list[str],
    ) -> dict[str, bytes] | None:
        actual_total = 0
        captured_members: dict[str, bytes] = {}
        for member in members:
            if member.is_dir():
                continue
            capture_limit = capture_limits.get(member.filename)
            member_limit = min(
                _WHEEL_MEMBER_ACTUAL_BYTES_LIMIT,
                capture_limit
                if capture_limit is not None
                else _WHEEL_MEMBER_ACTUAL_BYTES_LIMIT,
            )
            actual_member = 0
            captured = bytearray() if capture_limit is not None else None
            with archive.open(member, mode="r") as stream:
                while True:
                    read_size = min(
                        _STREAM_CHUNK_BYTES,
                        member_limit - actual_member + 1,
                        _WHEEL_AGGREGATE_ACTUAL_BYTES_LIMIT - actual_total + 1,
                    )
                    chunk = stream.read(read_size)
                    if not chunk:
                        break
                    actual_member += len(chunk)
                    actual_total += len(chunk)
                    if actual_member > member_limit:
                        if capture_limit is not None:
                            diagnostics.append(
                                f"wheel metadata member {member.filename!r} "
                                "exceeds metadata inspection limit"
                            )
                        else:
                            diagnostics.append(
                                f"wheel member {member.filename!r} actual "
                                "decompressed content exceeds per-member "
                                "inspection limit"
                            )
                        return None
                    if actual_total > _WHEEL_AGGREGATE_ACTUAL_BYTES_LIMIT:
                        diagnostics.append(
                            "wheel actual decompressed content exceeds aggregate "
                            "inspection limit"
                        )
                        return None
                    if captured is not None:
                        captured.extend(chunk)
            if captured is not None:
                captured_members[member.filename] = bytes(captured)
        return captured_members

    def _wheel_dist_info_root(
        self,
        members: list[zipfile.ZipInfo],
        diagnostics: list[str],
    ) -> str | None:
        dist_info_paths: set[tuple[str, ...]] = set()
        for member in members:
            parts = PurePosixPath(member.filename).parts
            for index, part in enumerate(parts):
                if part.endswith(".dist-info"):
                    dist_info_paths.add(parts[: index + 1])
        if len(dist_info_paths) != 1:
            diagnostics.append(
                "wheel must contain exactly one .dist-info metadata directory"
            )
            return None
        (dist_info_parts,) = tuple(dist_info_paths)
        if len(dist_info_parts) != 1:
            diagnostics.append("wheel .dist-info metadata directory is not top-level")
            return None
        return dist_info_parts[0]

    def _validate_wheel_metadata(
        self,
        members: list[zipfile.ZipInfo],
        dist_info_root: str,
        captured_members: dict[str, bytes],
        diagnostics: list[str],
    ) -> _PackageNameVersion | None:
        names = {member.filename for member in members}
        required = self._required_wheel_members(dist_info_root)
        missing = [label for label, name in required.items() if name not in names]
        for label in missing:
            diagnostics.append(f"wheel is missing required {label} metadata")

        identity: _PackageNameVersion | None = None
        metadata_path = required["METADATA"]
        if metadata_path in captured_members:
            metadata_text = self._decode_member_text(
                captured_members[metadata_path], "core METADATA", diagnostics
            )
            if metadata_text is not None:
                identity = self._parse_core_metadata(
                    metadata_text,
                    "wheel METADATA",
                    diagnostics,
                )

        wheel_path = required["WHEEL"]
        if wheel_path in captured_members:
            wheel_text = self._decode_member_text(
                captured_members[wheel_path], "WHEEL metadata", diagnostics
            )
            if wheel_text is not None:
                self._parse_wheel_metadata(wheel_text, diagnostics)

        record_path = required["RECORD"]
        if record_path in captured_members:
            record_text = self._decode_member_text(
                captured_members[record_path], "RECORD metadata", diagnostics
            )
            if record_text is not None:
                self._parse_record(record_text, required, diagnostics)
        return identity

    def _required_wheel_members(self, dist_info_root: str) -> dict[str, str]:
        return {
            "METADATA": f"{dist_info_root}/METADATA",
            "WHEEL": f"{dist_info_root}/WHEEL",
            "RECORD": f"{dist_info_root}/RECORD",
        }

    def _decode_member_text(
        self,
        content: bytes,
        label: str,
        diagnostics: list[str],
    ) -> str | None:
        try:
            return content.decode("utf-8")
        except UnicodeError as error:
            diagnostics.append(f"{label} is not valid UTF-8: {error}")
            return None

    def _parse_wheel_metadata(
        self,
        text: str,
        diagnostics: list[str],
    ) -> None:
        message = self._parse_message(text, "WHEEL metadata", diagnostics)
        if message is None:
            return
        wheel_version = self._single_header(
            message,
            "Wheel-Version",
            "WHEEL metadata",
            diagnostics,
        )
        root_is_purelib = self._single_header(
            message,
            "Root-Is-Purelib",
            "WHEEL metadata",
            diagnostics,
        )
        tags = tuple(str(value).strip() for value in message.get_all("Tag", []))
        if wheel_version is not None and not _METADATA_VERSION_PATTERN.fullmatch(
            wheel_version
        ):
            diagnostics.append("WHEEL metadata has malformed Wheel-Version")
        if root_is_purelib is not None and root_is_purelib.lower() not in {
            "true",
            "false",
        }:
            diagnostics.append("WHEEL metadata has malformed Root-Is-Purelib")
        if not tags:
            diagnostics.append("WHEEL metadata is missing Tag")
        for tag in tags:
            parts = tag.split("-")
            if len(parts) != 3 or any(
                not _WHEEL_TAG_COMPONENT_PATTERN.fullmatch(part) for part in parts
            ):
                diagnostics.append(f"WHEEL metadata has malformed Tag {tag!r}")

    def _parse_record(
        self,
        text: str,
        required: dict[str, str],
        diagnostics: list[str],
    ) -> None:
        try:
            rows = tuple(csv.reader(io.StringIO(text, newline=""), strict=True))
        except csv.Error as error:
            diagnostics.append(f"wheel RECORD is malformed CSV: {error}")
            return
        if not rows:
            diagnostics.append("wheel RECORD contains no file entries")
            return
        record_paths: list[str] = []
        for row_number, row in enumerate(rows, start=1):
            if len(row) != 3 or not row[0]:
                diagnostics.append(
                    f"wheel RECORD row {row_number} must contain path, hash, and size"
                )
                continue
            path_diagnostic = self._archive_path_diagnostic(row[0])
            if path_diagnostic is not None:
                diagnostics.append(
                    f"wheel RECORD path {row[0]!r} is unsafe: {path_diagnostic}"
                )
            record_paths.append(row[0])
        normalized_record_paths = [
            self._normalized_archive_member_name(path) for path in record_paths
        ]
        duplicate_paths = sorted(
            path
            for path, count in Counter(normalized_record_paths).items()
            if count > 1
        )
        for path in duplicate_paths:
            diagnostics.append(
                f"wheel RECORD contains duplicate normalized path {path!r}"
            )
        record_path_set = set(record_paths)
        for label, required_path in required.items():
            if required_path not in record_path_set:
                diagnostics.append(f"wheel RECORD does not list required {label}")

    def _compare_dist_info_identity(
        self,
        dist_info_root: str,
        metadata_identity: _PackageNameVersion | None,
        diagnostics: list[str],
    ) -> None:
        stem = dist_info_root.removesuffix(".dist-info")
        if "-" not in stem:
            diagnostics.append("wheel .dist-info directory has malformed name")
            return
        name, version = stem.rsplit("-", 1)
        dist_info_identity = _PackageNameVersion(name, version)
        self._compare_identities(
            "wheel .dist-info directory",
            dist_info_identity,
            "wheel package metadata",
            metadata_identity,
            diagnostics,
        )

    def _stream_sdist_archive(
        self,
        path: Path,
        diagnostics: list[str],
    ) -> _SdistStreamInspection | None:
        roots: set[str] = set()
        normalized_names: set[str] = set()
        regular_member_names: set[str] = set()
        captured_members: dict[str, bytes] = {}
        has_python_source = False

        with (
            path.open("rb") as raw_archive,
            gzip.GzipFile(fileobj=raw_archive, mode="rb") as decompressed,
        ):
            bounded_stream = _ActualByteLimitReader(
                cast(BinaryIO, decompressed),
                _SDIST_AGGREGATE_ACTUAL_BYTES_LIMIT,
                "source archive actual decompressed content exceeds "
                "aggregate inspection limit",
            )
            with tarfile.open(
                fileobj=cast(BinaryIO, bounded_stream),
                mode="r|",
                bufsize=_STREAM_CHUNK_BYTES,
            ) as archive:
                for member_count, member in enumerate(archive, start=1):
                    if member_count > _ARCHIVE_MEMBER_COUNT_LIMIT:
                        diagnostics.append(
                            "source archive exceeds "
                            f"{_ARCHIVE_MEMBER_COUNT_LIMIT}-member "
                            "inspection limit"
                        )
                        return None
                    path_diagnostic = self._archive_path_diagnostic(member.name)
                    if path_diagnostic is not None:
                        diagnostics.append(
                            f"source archive member {member.name!r} has unsafe "
                            f"path: {path_diagnostic}"
                        )
                        return None
                    normalized_name = self._normalized_archive_member_name(member.name)
                    if normalized_name in normalized_names:
                        diagnostics.append(
                            "source archive contains duplicate normalized "
                            f"member path {normalized_name!r}"
                        )
                        return None
                    normalized_names.add(normalized_name)
                    if not (member.isfile() or member.isdir()):
                        diagnostics.append(
                            f"source archive member {member.name!r} is not a "
                            "regular file or directory"
                        )
                        return None

                    parts = PurePosixPath(member.name).parts
                    roots.add(parts[0])
                    if member.isdir():
                        continue
                    regular_member_names.add(member.name)
                    has_python_source = has_python_source or member.name.endswith(".py")
                    capture_limit = (
                        _CORE_METADATA_BYTES_LIMIT
                        if len(parts) == 2
                        and parts[1] in {"PKG-INFO", "pyproject.toml"}
                        else None
                    )
                    captured = self._stream_tar_member(
                        archive,
                        member,
                        capture_limit,
                    )
                    if captured is not None:
                        captured_members[member.name] = captured

                while bounded_stream.read(_STREAM_CHUNK_BYTES):
                    pass

        return _SdistStreamInspection(
            roots=frozenset(roots),
            regular_member_names=frozenset(regular_member_names),
            captured_members=captured_members,
            has_python_source=has_python_source,
        )

    def _stream_tar_member(
        self,
        archive: tarfile.TarFile,
        member: tarfile.TarInfo,
        capture_limit: int | None,
    ) -> bytes | None:
        stream = archive.extractfile(member)
        if stream is None:
            raise tarfile.ReadError(f"cannot read member {member.name!r}")
        member_limit = min(
            _SDIST_MEMBER_ACTUAL_BYTES_LIMIT,
            capture_limit
            if capture_limit is not None
            else _SDIST_MEMBER_ACTUAL_BYTES_LIMIT,
        )
        actual_member = 0
        captured = bytearray() if capture_limit is not None else None
        while True:
            chunk = stream.read(
                min(_STREAM_CHUNK_BYTES, member_limit - actual_member + 1)
            )
            if not chunk:
                break
            actual_member += len(chunk)
            if actual_member > member_limit:
                if capture_limit is not None:
                    diagnostic = (
                        f"source metadata member {member.name!r} exceeds metadata "
                        "inspection limit"
                    )
                else:
                    diagnostic = (
                        f"source archive member {member.name!r} actual content "
                        "exceeds per-member inspection limit"
                    )
                raise _StructuralInspectionLimitExceeded(diagnostic)
            if captured is not None:
                captured.extend(chunk)
        return bytes(captured) if captured is not None else None

    def _sdist_package_root(
        self,
        roots: frozenset[str],
        diagnostics: list[str],
    ) -> str | None:
        if len(roots) != 1:
            diagnostics.append("source archive must contain one package root")
            return None
        return next(iter(roots))

    def _validate_sdist_content(
        self,
        stream_inspection: _SdistStreamInspection,
        package_root: str,
        diagnostics: list[str],
    ) -> tuple[_PackageNameVersion | None, _PackageNameVersion | None]:
        pkg_info_path = f"{package_root}/PKG-INFO"
        pyproject_path = f"{package_root}/pyproject.toml"
        for label, path in (
            ("PKG-INFO", pkg_info_path),
            ("pyproject.toml", pyproject_path),
        ):
            if path not in stream_inspection.regular_member_names:
                diagnostics.append(f"source archive is missing required {label} file")
        if not stream_inspection.has_python_source:
            diagnostics.append("source archive contains no Python source modules")

        metadata_identity: _PackageNameVersion | None = None
        if pkg_info_path in stream_inspection.captured_members:
            pkg_info_text = self._decode_member_text(
                stream_inspection.captured_members[pkg_info_path],
                "source PKG-INFO",
                diagnostics,
            )
            if pkg_info_text is not None:
                metadata_identity = self._parse_core_metadata(
                    pkg_info_text,
                    "source PKG-INFO",
                    diagnostics,
                )

        source_identity: _PackageNameVersion | None = None
        if pyproject_path in stream_inspection.captured_members:
            pyproject_text = self._decode_member_text(
                stream_inspection.captured_members[pyproject_path],
                "archived pyproject.toml",
                diagnostics,
            )
            if pyproject_text is not None:
                try:
                    source_identity = self._parse_pyproject_identity(pyproject_text)
                except (tomllib.TOMLDecodeError, ValueError) as error:
                    diagnostics.append(f"archived pyproject.toml is malformed: {error}")
        return metadata_identity, source_identity

    def _compare_sdist_root_identity(
        self,
        package_root: str,
        metadata_identity: _PackageNameVersion | None,
        diagnostics: list[str],
    ) -> None:
        if "-" not in package_root:
            diagnostics.append("source archive package root has malformed name")
            return
        name, version = package_root.rsplit("-", 1)
        root_identity = _PackageNameVersion(name, version)
        self._compare_identities(
            "source archive package root",
            root_identity,
            "source-distribution package metadata",
            metadata_identity,
            diagnostics,
        )

    def _parse_core_metadata(
        self,
        text: str,
        label: str,
        diagnostics: list[str],
    ) -> _PackageNameVersion | None:
        message = self._parse_message(text, label, diagnostics)
        if message is None:
            return None
        metadata_version = self._single_header(
            message,
            "Metadata-Version",
            label,
            diagnostics,
        )
        name = self._single_header(message, "Name", label, diagnostics)
        version = self._single_header(message, "Version", label, diagnostics)
        if metadata_version is not None and not _METADATA_VERSION_PATTERN.fullmatch(
            metadata_version
        ):
            diagnostics.append(f"{label} has malformed Metadata-Version")
        if name is None or version is None:
            return None
        return _PackageNameVersion(name, version)

    def _parse_message(
        self,
        text: str,
        label: str,
        diagnostics: list[str],
    ) -> Message | None:
        message = Parser(policy=default).parsestr(text)
        if message.defects:
            defect_names = ", ".join(
                type(defect).__name__ for defect in message.defects
            )
            diagnostics.append(f"{label} is malformed: {defect_names}")
            return None
        return message

    def _single_header(
        self,
        message: Message,
        header: str,
        label: str,
        diagnostics: list[str],
    ) -> str | None:
        values = tuple(str(value).strip() for value in message.get_all(header, []))
        if len(values) != 1 or not values[0]:
            diagnostics.append(f"{label} must contain exactly one {header} field")
            return None
        return values[0]

    def _parse_pyproject_identity(self, text: str) -> _PackageNameVersion:
        document = tomllib.loads(text)
        project = document.get("project")
        if not isinstance(project, dict):
            raise ValueError("pyproject.toml does not contain a [project] table")
        name = project.get("name")
        version = project.get("version")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("pyproject.toml project.name is missing or invalid")
        if not isinstance(version, str) or not version.strip():
            raise ValueError("pyproject.toml project.version is missing or invalid")
        return _PackageNameVersion(name.strip(), version.strip())

    def _parse_wheel_filename(
        self,
        filename: str,
        diagnostics: list[str],
    ) -> _PackageNameVersion | None:
        if not filename.endswith(".whl"):
            diagnostics.append("wheel filename must end with .whl")
            return None
        parts = filename.removesuffix(".whl").split("-")
        if len(parts) not in {5, 6} or any(not part for part in parts):
            diagnostics.append("wheel filename does not match the wheel file format")
            return None
        if len(parts) == 6 and not parts[2][0].isdigit():
            diagnostics.append("wheel filename has malformed build tag")
        for component in parts[-3:]:
            if not _WHEEL_TAG_COMPONENT_PATTERN.fullmatch(component):
                diagnostics.append("wheel filename has malformed compatibility tags")
                break
        return _PackageNameVersion(parts[0], parts[1])

    def _parse_sdist_filename(
        self,
        filename: str,
        diagnostics: list[str],
    ) -> _PackageNameVersion | None:
        if not filename.endswith(".tar.gz"):
            diagnostics.append("source-distribution filename must end with .tar.gz")
            return None
        stem = filename.removesuffix(".tar.gz")
        if "-" not in stem:
            diagnostics.append(
                "source-distribution filename must contain package name and version"
            )
            return None
        name, version = stem.rsplit("-", 1)
        if not name or not version:
            diagnostics.append(
                "source-distribution filename has empty package name or version"
            )
            return None
        return _PackageNameVersion(name, version)

    def _compare_expected_identity(
        self,
        actual: _PackageNameVersion | None,
        expected: _PackageNameVersion | None,
        diagnostics: list[str],
    ) -> None:
        if actual is None or expected is None:
            return
        if not self._identities_equal(actual, expected):
            diagnostics.append(
                "package name/version does not match authoritative pyproject.toml "
                f"({actual.name} {actual.version} != "
                f"{expected.name} {expected.version})"
            )

    def _compare_identities(
        self,
        left_label: str,
        left: _PackageNameVersion | None,
        right_label: str,
        right: _PackageNameVersion | None,
        diagnostics: list[str],
    ) -> None:
        if left is None or right is None or self._identities_equal(left, right):
            return
        diagnostics.append(
            f"{left_label} name/version does not match {right_label} "
            f"({left.name} {left.version} != {right.name} {right.version})"
        )

    def _add_cross_artifact_findings(
        self,
        inspections: list[_CandidateInspection],
    ) -> list[_CandidateInspection]:
        identities = [
            inspection for inspection in inspections if inspection.identity is not None
        ]
        if len(identities) < 2:
            return inspections
        reference = identities[0]
        mismatched = [
            inspection
            for inspection in identities[1:]
            if not self._identities_equal(
                reference.identity,
                inspection.identity,
            )
        ]
        if not mismatched:
            return inspections
        affected = {
            reference.candidate.path,
            *(item.candidate.path for item in mismatched),
        }
        return [
            _CandidateInspection(
                candidate=inspection.candidate,
                identity=inspection.identity,
                diagnostics=(
                    *inspection.diagnostics,
                    "wheel and source-distribution package name/version do not match",
                ),
            )
            if inspection.candidate.path in affected
            else inspection
            for inspection in inspections
        ]

    def _identities_equal(
        self,
        left: _PackageNameVersion | None,
        right: _PackageNameVersion | None,
    ) -> bool:
        if left is None or right is None:
            return False
        return (
            self._normalize_distribution_name(left.name)
            == self._normalize_distribution_name(right.name)
            and left.version == right.version
        )

    def _normalize_distribution_name(self, name: str) -> str:
        return re.sub(r"[-_.]+", "-", name).lower()

    def _normalized_archive_member_name(self, name: str) -> str:
        return name[:-1] if name.endswith("/") else name

    def _archive_path_diagnostic(self, name: str) -> str | None:
        if not name or "\x00" in name:
            return "empty or NUL-containing member name"
        if "\\" in name:
            return "backslash-separated member name"
        path = PurePosixPath(name)
        if path.is_absolute():
            return "absolute member name"
        trimmed = name[:-1] if name.endswith("/") else name
        parts = trimmed.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            return "non-canonical or traversal-like member name"
        if parts[0].endswith(":"):
            return "drive-qualified member name"
        return None
