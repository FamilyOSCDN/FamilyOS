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

from packaging.markers import InvalidMarker, Marker
from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

from familyos_cli.application.build.artifact_discovery import (
    DiscoveredArtifact,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.package_identity import PackageIdentity
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
_IGNORED_SOURCE_DIRECTORY_NAMES = frozenset(
    {"__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
)
_IGNORED_SOURCE_FILE_NAMES = frozenset({".DS_Store", "Thumbs.db"})
_IGNORED_SOURCE_FILE_SUFFIXES = frozenset({".pyc", ".pyo", ".swp", ".swo"})
_GENERATED_SDIST_ROOT_FILES = frozenset({"PKG-INFO", "setup.cfg"})
_GENERATED_EGG_INFO_FILES = frozenset(
    {
        "PKG-INFO",
        "SOURCES.txt",
        "dependency_links.txt",
        "entry_points.txt",
        "requires.txt",
        "top_level.txt",
    }
)


@dataclass(frozen=True, slots=True)
class _PackageNameVersion:
    name: str
    version: str


@dataclass(frozen=True, slots=True)
class _ProjectPackageMetadata:
    identity: _PackageNameVersion
    requires_python: str
    requirements: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _CoreMetadataInspection:
    identity: _PackageNameVersion | None
    requires_python: str | None
    requirements: tuple[str, ...]
    requirements_valid: bool


@dataclass(frozen=True, slots=True)
class _ExpectedPackageContent:
    source_base: str
    python_modules: frozenset[str]
    resources: frozenset[str]
    sdist_project_files: frozenset[str]
    generated_egg_info_root: str

    @property
    def package_files(self) -> frozenset[str]:
        """Return the complete expected installable package inventory."""

        return self.python_modules | self.resources


@dataclass(frozen=True, slots=True)
class _ProjectPackageContract:
    metadata: _ProjectPackageMetadata
    content: _ExpectedPackageContent


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

        expected, authority_diagnostic = self._load_project_contract()
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
                package_identity=(
                    PackageIdentity(
                        name=inspection.identity.name,
                        version=inspection.identity.version,
                    )
                    if inspection.identity is not None
                    and not inspection.diagnostics
                    else None
                ),
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

    def _load_project_contract(
        self,
    ) -> tuple[_ProjectPackageContract | None, str | None]:
        pyproject_path = self._project_root / "pyproject.toml"
        try:
            pyproject_text = pyproject_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return None, "authoritative pyproject.toml is unreadable"
        try:
            document = tomllib.loads(pyproject_text)
            metadata = self._parse_project_metadata(document)
            content = self._load_expected_package_content(document, metadata.identity)
            return _ProjectPackageContract(metadata, content), None
        except tomllib.TOMLDecodeError:
            return None, "authoritative pyproject.toml is malformed"
        except ValueError as error:
            return None, str(error)

    def _inspect_candidate(
        self,
        candidate: DiscoveredArtifact,
        expected: _ProjectPackageContract | None,
        authority_diagnostic: str | None,
    ) -> _CandidateInspection:
        if authority_diagnostic is not None:
            return _CandidateInspection(
                candidate=candidate,
                identity=None,
                diagnostics=(authority_diagnostic,),
            )
        if expected is None:
            return _CandidateInspection(
                candidate=candidate,
                identity=None,
                diagnostics=("authoritative package contract is unavailable",),
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
        expected: _ProjectPackageContract,
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
                        expected.metadata,
                        diagnostics,
                    )
                    self._compare_dist_info_identity(
                        dist_info_root,
                        metadata_identity,
                        diagnostics,
                    )
                    self._validate_wheel_content(
                        members,
                        dist_info_root,
                        expected.content,
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
        self._compare_expected_identity(
            identity,
            expected.metadata.identity,
            diagnostics,
        )
        return _CandidateInspection(candidate, identity, tuple(diagnostics))

    def _inspect_sdist(
        self,
        candidate: DiscoveredArtifact,
        expected: _ProjectPackageContract,
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
                        expected,
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
        self._compare_expected_identity(
            identity,
            expected.metadata.identity,
            diagnostics,
        )
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
        expected: _ProjectPackageMetadata,
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
                metadata = self._parse_core_metadata(
                    metadata_text,
                    "wheel METADATA",
                    diagnostics,
                )
                identity = metadata.identity
                self._compare_package_metadata(
                    "wheel METADATA",
                    metadata,
                    expected,
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

    def _validate_wheel_content(
        self,
        members: list[zipfile.ZipInfo],
        dist_info_root: str,
        expected: _ExpectedPackageContent,
        diagnostics: list[str],
    ) -> None:
        actual = frozenset(
            member.filename
            for member in members
            if not member.is_dir()
            and not member.filename.startswith(f"{dist_info_root}/")
        )
        self._compare_package_content(
            "wheel",
            actual,
            expected.python_modules,
            expected.resources,
            diagnostics,
        )

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
        expected: _ProjectPackageContract,
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

        self._validate_sdist_inventory(
            stream_inspection.regular_member_names,
            package_root,
            expected.content,
            diagnostics,
        )

        metadata_identity: _PackageNameVersion | None = None
        if pkg_info_path in stream_inspection.captured_members:
            pkg_info_text = self._decode_member_text(
                stream_inspection.captured_members[pkg_info_path],
                "source PKG-INFO",
                diagnostics,
            )
            if pkg_info_text is not None:
                metadata = self._parse_core_metadata(
                    pkg_info_text,
                    "source PKG-INFO",
                    diagnostics,
                )
                metadata_identity = metadata.identity
                self._compare_package_metadata(
                    "source PKG-INFO",
                    metadata,
                    expected.metadata,
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
                    source_metadata = self._parse_project_metadata(
                        tomllib.loads(pyproject_text)
                    )
                    source_identity = source_metadata.identity
                    self._compare_project_metadata(
                        "archived pyproject.toml",
                        source_metadata,
                        expected.metadata,
                        diagnostics,
                    )
                except (tomllib.TOMLDecodeError, ValueError) as error:
                    diagnostics.append(f"archived pyproject.toml is malformed: {error}")
        return metadata_identity, source_identity

    def _validate_sdist_inventory(
        self,
        member_names: frozenset[str],
        package_root: str,
        expected: _ExpectedPackageContent,
        diagnostics: list[str],
    ) -> None:
        source_prefix = f"{package_root}/{expected.source_base}/"
        egg_info_prefix = f"{source_prefix}{expected.generated_egg_info_root}/"
        actual_package_files = frozenset(
            name.removeprefix(source_prefix)
            for name in member_names
            if name.startswith(source_prefix) and not name.startswith(egg_info_prefix)
        )
        self._compare_package_content(
            "source archive",
            actual_package_files,
            expected.python_modules,
            expected.resources,
            diagnostics,
        )

        allowed_project_files = {
            f"{package_root}/{name}" for name in expected.sdist_project_files
        }
        allowed_generated_files = {
            f"{package_root}/{name}" for name in _GENERATED_SDIST_ROOT_FILES
        }
        unexpected_project_files = sorted(
            name
            for name in member_names
            if not name.startswith(source_prefix)
            and name not in allowed_project_files
            and name not in allowed_generated_files
        )
        unexpected_egg_info_files = sorted(
            name
            for name in member_names
            if name.startswith(egg_info_prefix)
            and name.removeprefix(egg_info_prefix) not in _GENERATED_EGG_INFO_FILES
        )
        for name in (*unexpected_project_files, *unexpected_egg_info_files):
            diagnostics.append(
                f"source archive contains unintended source-distribution content "
                f"{name!r}"
            )

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
    ) -> _CoreMetadataInspection:
        message = self._parse_message(text, label, diagnostics)
        if message is None:
            return _CoreMetadataInspection(None, None, (), False)
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
        identity = (
            _PackageNameVersion(name, version)
            if name is not None and version is not None
            else None
        )
        if version is not None:
            try:
                Version(version)
            except InvalidVersion:
                diagnostics.append(f"{label} has malformed Version {version!r}")
                identity = None

        requires_python = self._parse_requires_python_header(
            message,
            label,
            diagnostics,
        )
        requirements, requirements_valid = self._parse_requires_dist_headers(
            message,
            label,
            diagnostics,
        )
        return _CoreMetadataInspection(
            identity,
            requires_python,
            requirements,
            requirements_valid,
        )

    def _parse_requires_python_header(
        self,
        message: Message,
        label: str,
        diagnostics: list[str],
    ) -> str | None:
        values = tuple(
            str(value).strip() for value in message.get_all("Requires-Python", [])
        )
        if len(values) != 1 or not values[0]:
            diagnostics.append(
                f"{label} must contain exactly one Requires-Python field"
            )
            return None
        try:
            return str(SpecifierSet(values[0]))
        except InvalidSpecifier:
            diagnostics.append(
                f"{label} contains malformed Requires-Python {values[0]!r}"
            )
            return None

    def _parse_requires_dist_headers(
        self,
        message: Message,
        label: str,
        diagnostics: list[str],
    ) -> tuple[tuple[str, ...], bool]:
        requirements: list[str] = []
        valid = True
        for value in (
            str(item).strip() for item in message.get_all("Requires-Dist", [])
        ):
            try:
                requirements.append(self._normalize_requirement(Requirement(value)))
            except InvalidRequirement:
                diagnostics.append(
                    f"{label} contains malformed Requires-Dist {value!r}"
                )
                valid = False
        return tuple(sorted(requirements)), valid

    def _compare_package_metadata(
        self,
        label: str,
        actual: _CoreMetadataInspection,
        expected: _ProjectPackageMetadata,
        diagnostics: list[str],
    ) -> None:
        if (
            actual.requires_python is not None
            and actual.requires_python != expected.requires_python
        ):
            diagnostics.append(
                f"{label} Requires-Python does not match authoritative "
                f"pyproject.toml ({actual.requires_python!r} != "
                f"{expected.requires_python!r})"
            )
        if actual.requirements_valid:
            self._compare_requirement_sets(
                label,
                actual.requirements,
                expected.requirements,
                diagnostics,
            )

    def _compare_project_metadata(
        self,
        label: str,
        actual: _ProjectPackageMetadata,
        expected: _ProjectPackageMetadata,
        diagnostics: list[str],
    ) -> None:
        if actual.requires_python != expected.requires_python:
            diagnostics.append(
                f"{label} Requires-Python does not match authoritative "
                f"pyproject.toml ({actual.requires_python!r} != "
                f"{expected.requires_python!r})"
            )
        self._compare_requirement_sets(
            label,
            actual.requirements,
            expected.requirements,
            diagnostics,
        )

    def _compare_requirement_sets(
        self,
        label: str,
        actual: tuple[str, ...],
        expected: tuple[str, ...],
        diagnostics: list[str],
    ) -> None:
        missing = Counter(expected) - Counter(actual)
        unexpected = Counter(actual) - Counter(expected)
        for requirement in sorted(missing.elements()):
            diagnostics.append(
                f"{label} is missing authoritative Requires-Dist {requirement!r}"
            )
        for requirement in sorted(unexpected.elements()):
            diagnostics.append(
                f"{label} contains unexpected Requires-Dist {requirement!r}"
            )

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

    def _parse_project_metadata(
        self,
        document: dict[str, object],
    ) -> _ProjectPackageMetadata:
        project = document.get("project")
        if not isinstance(project, dict):
            raise ValueError("pyproject.toml does not contain a [project] table")
        name = project.get("name")
        version = project.get("version")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("pyproject.toml project.name is missing or invalid")
        if not isinstance(version, str) or not version.strip():
            raise ValueError("pyproject.toml project.version is missing or invalid")
        try:
            Version(version.strip())
        except InvalidVersion as error:
            raise ValueError("pyproject.toml project.version is malformed") from error

        requires_python = project.get("requires-python")
        if not isinstance(requires_python, str) or not requires_python.strip():
            raise ValueError(
                "pyproject.toml project.requires-python is missing or invalid"
            )
        try:
            normalized_requires_python = str(SpecifierSet(requires_python))
        except InvalidSpecifier as error:
            raise ValueError(
                "pyproject.toml project.requires-python is malformed"
            ) from error

        requirements = self._parse_project_requirements(project)
        return _ProjectPackageMetadata(
            identity=_PackageNameVersion(name.strip(), version.strip()),
            requires_python=normalized_requires_python,
            requirements=requirements,
        )

    def _parse_project_requirements(
        self,
        project: dict[str, object],
    ) -> tuple[str, ...]:
        requirements: list[str] = []
        dependencies = project.get("dependencies", [])
        if not isinstance(dependencies, list) or not all(
            isinstance(value, str) for value in dependencies
        ):
            raise ValueError("pyproject.toml project.dependencies is invalid")
        for value in dependencies:
            requirements.append(
                self._parse_project_requirement(value, "project.dependencies")
            )

        optional_dependencies = project.get("optional-dependencies", {})
        if not isinstance(optional_dependencies, dict):
            raise ValueError("pyproject.toml project.optional-dependencies is invalid")
        for extra, values in sorted(optional_dependencies.items()):
            if (
                not isinstance(extra, str)
                or not isinstance(values, list)
                or not all(isinstance(value, str) for value in values)
            ):
                raise ValueError(
                    "pyproject.toml project.optional-dependencies is invalid"
                )
            for value in values:
                try:
                    requirement = Requirement(value)
                    extra_marker = Marker(f'extra == "{canonicalize_name(extra)}"')
                    marker = (
                        Marker(f"({requirement.marker}) and ({extra_marker})")
                        if requirement.marker is not None
                        else extra_marker
                    )
                except (InvalidRequirement, InvalidMarker) as error:
                    raise ValueError(
                        "pyproject.toml optional dependency contains malformed "
                        f"requirement {value!r}"
                    ) from error
                requirements.append(
                    self._normalize_requirement(requirement, marker=marker)
                )
        return tuple(sorted(requirements))

    def _parse_project_requirement(self, value: str, label: str) -> str:
        try:
            return self._normalize_requirement(Requirement(value))
        except InvalidRequirement as error:
            raise ValueError(
                f"pyproject.toml {label} contains malformed requirement {value!r}"
            ) from error

    def _normalize_requirement(
        self,
        requirement: Requirement,
        *,
        marker: Marker | None = None,
    ) -> str:
        name = canonicalize_name(requirement.name)
        extras = ""
        if requirement.extras:
            extras = (
                "["
                + ",".join(
                    sorted(canonicalize_name(extra) for extra in requirement.extras)
                )
                + "]"
            )
        if requirement.url is not None:
            normalized = f"{name}{extras} @ {requirement.url}"
        else:
            normalized = f"{name}{extras}{requirement.specifier}"
        effective_marker = marker if marker is not None else requirement.marker
        if effective_marker is not None:
            normalized += f"; {effective_marker}"
        return normalized

    def _load_expected_package_content(
        self,
        document: dict[str, object],
        identity: _PackageNameVersion,
    ) -> _ExpectedPackageContent:
        source_base = self._setuptools_source_base(document)
        source_base_path = self._project_root / source_base
        if not source_base_path.is_dir() or source_base_path.is_symlink():
            raise ValueError(
                "authoritative setuptools package source directory is unavailable"
            )
        package_roots = tuple(
            sorted(
                child
                for child in source_base_path.iterdir()
                if child.is_dir()
                and not child.is_symlink()
                and (child / "__init__.py").is_file()
            )
        )
        if not package_roots:
            raise ValueError(
                "authoritative setuptools package source contains no packages"
            )

        package_source_files = frozenset(
            path.relative_to(source_base_path).as_posix()
            for package_root in package_roots
            for path in package_root.rglob("*")
            if self._is_authoritative_package_source_file(path, package_root)
        )
        python_modules = frozenset(
            path for path in package_source_files if path.endswith(".py")
        )
        resources = self._load_expected_package_resources(
            document,
            source_base_path,
            package_roots,
        )
        if not python_modules:
            raise ValueError(
                "authoritative setuptools package source contains no Python modules"
            )

        return _ExpectedPackageContent(
            source_base=source_base,
            python_modules=python_modules,
            resources=resources,
            sdist_project_files=self._expected_sdist_project_files(document),
            generated_egg_info_root=(
                canonicalize_name(identity.name).replace("-", "_") + ".egg-info"
            ),
        )

    def _setuptools_source_base(self, document: dict[str, object]) -> str:
        tool = document.get("tool")
        setuptools = tool.get("setuptools") if isinstance(tool, dict) else None
        package_dir = (
            setuptools.get("package-dir") if isinstance(setuptools, dict) else None
        )
        source_base = package_dir.get("") if isinstance(package_dir, dict) else None
        if not isinstance(source_base, str):
            raise ValueError(
                "pyproject.toml tool.setuptools.package-dir[''] is missing or invalid"
            )
        source_base = source_base.rstrip("/")
        if self._archive_path_diagnostic(source_base) is not None:
            raise ValueError(
                "pyproject.toml tool.setuptools package source path is unsafe"
            )

        packages = setuptools.get("packages") if isinstance(setuptools, dict) else None
        find = packages.get("find") if isinstance(packages, dict) else None
        where = find.get("where") if isinstance(find, dict) else None
        if not isinstance(where, list) or source_base not in where:
            raise ValueError(
                "pyproject.toml setuptools package discovery does not match "
                "package-dir authority"
            )
        return source_base

    def _is_authoritative_package_source_file(
        self,
        path: Path,
        package_root: Path,
    ) -> bool:
        if not path.is_file() or path.is_symlink():
            return False
        relative_parts = path.relative_to(package_root).parts
        if any(
            part in _IGNORED_SOURCE_DIRECTORY_NAMES or part.endswith(".egg-info")
            for part in relative_parts[:-1]
        ):
            return False
        if path.name in _IGNORED_SOURCE_FILE_NAMES or path.name.endswith("~"):
            return False
        return path.suffix not in _IGNORED_SOURCE_FILE_SUFFIXES

    def _load_expected_package_resources(
        self,
        document: dict[str, object],
        source_base_path: Path,
        package_roots: tuple[Path, ...],
    ) -> frozenset[str]:
        """Resolve intended non-code resources from setuptools package-data.

        This intentionally supports the repository's current policy shape:
        exact discovered package names mapped to relative ``pathlib`` glob
        patterns. Source existence alone does not establish packaging intent.
        """

        tool = document.get("tool")
        setuptools = tool.get("setuptools") if isinstance(tool, dict) else None
        package_data = (
            setuptools.get("package-data") if isinstance(setuptools, dict) else None
        )
        if package_data is None:
            return frozenset()
        if not isinstance(package_data, dict) or not all(
            isinstance(name, str) for name in package_data
        ):
            raise ValueError("pyproject.toml tool.setuptools.package-data is invalid")

        packages_by_name = {
            ".".join(package_root.relative_to(source_base_path).parts): package_root
            for package_root in package_roots
        }
        resources: set[str] = set()
        for package_name in sorted(package_data):
            patterns = package_data[package_name]
            package_root = packages_by_name.get(package_name)
            if package_root is None:
                raise ValueError(
                    "pyproject.toml tool.setuptools.package-data uses unsupported "
                    f"package key {package_name!r}"
                )
            if not isinstance(patterns, list) or not all(
                isinstance(pattern, str) and pattern for pattern in patterns
            ):
                raise ValueError(
                    "pyproject.toml tool.setuptools.package-data patterns are invalid"
                )
            for pattern in patterns:
                if self._archive_path_diagnostic(pattern) is not None:
                    raise ValueError(
                        "pyproject.toml tool.setuptools.package-data contains unsafe "
                        f"pattern {pattern!r}"
                    )
                for path in package_root.glob(pattern):
                    if (
                        not self._is_authoritative_package_source_file(
                            path, package_root
                        )
                        or path.suffix == ".py"
                    ):
                        continue
                    resources.add(path.relative_to(source_base_path).as_posix())
        return frozenset(resources)

    def _expected_sdist_project_files(
        self,
        document: dict[str, object],
    ) -> frozenset[str]:
        expected = {"pyproject.toml"}
        project = document.get("project")
        if not isinstance(project, dict):
            return frozenset(expected)
        readme = project.get("readme")
        if isinstance(readme, str):
            expected.add(readme)
        elif isinstance(readme, dict):
            readme_file = readme.get("file")
            if isinstance(readme_file, str):
                expected.add(readme_file)
        for pattern in ("LICEN[CS]E*", "COPYING*", "NOTICE*", "AUTHORS*"):
            expected.update(
                path.name
                for path in self._project_root.glob(pattern)
                if path.is_file() and not path.is_symlink()
            )
        return frozenset(expected)

    def _compare_package_content(
        self,
        label: str,
        actual: frozenset[str],
        expected_python_modules: frozenset[str],
        expected_resources: frozenset[str],
        diagnostics: list[str],
    ) -> None:
        expected = expected_python_modules | expected_resources
        for path in sorted(expected_python_modules - actual):
            diagnostics.append(f"{label} is missing expected Python module {path!r}")
        for path in sorted(expected_resources - actual):
            diagnostics.append(f"{label} is missing required package resource {path!r}")
        for path in sorted(actual - expected):
            content_kind = (
                "Python module" if path.endswith(".py") else "package resource"
            )
            diagnostics.append(f"{label} contains unintended {content_kind} {path!r}")

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
        try:
            versions_match = Version(left.version) == Version(right.version)
        except InvalidVersion:
            return False
        return (
            canonicalize_name(left.name) == canonicalize_name(right.name)
            and versions_match
        )

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
