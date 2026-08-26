"""Deterministic semantic content inspection for package artifacts."""

from __future__ import annotations

import gzip
import hashlib
import stat
import tarfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO, cast

from familyos_cli.application.build.artifact_content_snapshot import (
    ArtifactContentMember,
    ArtifactContentSnapshot,
)
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
)
from familyos_cli.application.build.artifact_type import ArtifactClass

_STREAM_CHUNK_BYTES = 65_536
_ARCHIVE_MEMBER_COUNT_LIMIT = 10_000
_MEMBER_ACTUAL_BYTES_LIMIT = 67_108_864
_AGGREGATE_ACTUAL_BYTES_LIMIT = 536_870_912
_SUPPORTED_WHEEL_COMPRESSION = frozenset({zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED})


class ArtifactContentSnapshotError(ValueError):
    """Raised when semantic artifact content cannot be inspected safely."""


class ArtifactContentSnapshotter:
    """Calculate deterministic semantic content snapshots."""

    def snapshot(
        self,
        path: Path,
        artifact_type: ArtifactClass,
    ) -> ArtifactContentSnapshot:
        """Calculate semantic content identity for one package artifact."""

        if artifact_type is ArtifactClass.PYTHON_WHEEL:
            return self._snapshot_wheel(path)

        if artifact_type is ArtifactClass.SOURCE_DISTRIBUTION:
            return self._snapshot_sdist(path)

        raise ArtifactContentSnapshotError(
            f"unsupported artifact type: {artifact_type}"
        )

    def _snapshot_wheel(self, path: Path) -> ArtifactContentSnapshot:
        members: list[ArtifactContentMember] = []
        actual_total = 0

        try:
            with zipfile.ZipFile(path) as archive:
                infos = archive.infolist()

                if len(infos) > _ARCHIVE_MEMBER_COUNT_LIMIT:
                    raise ArtifactContentSnapshotError(
                        "wheel exceeds archive member inspection limit"
                    )

                normalized_names: set[str] = set()

                for info in infos:
                    name = self._normalized_archive_member_name(info.filename)
                    self._require_safe_path(name)

                    if name in normalized_names:
                        raise ArtifactContentSnapshotError(
                            f"wheel contains duplicate normalized member path {name!r}"
                        )
                    normalized_names.add(name)

                    self._require_safe_zip_type(info)

                    if info.is_dir():
                        continue

                    if info.compress_type not in _SUPPORTED_WHEEL_COMPRESSION:
                        raise ArtifactContentSnapshotError(
                            f"wheel member {info.filename!r} uses unsupported "
                            "compression"
                        )

                    member_hasher = hashlib.sha256()
                    actual_member = 0

                    with archive.open(info, mode="r") as stream:
                        while True:
                            read_size = min(
                                _STREAM_CHUNK_BYTES,
                                _MEMBER_ACTUAL_BYTES_LIMIT - actual_member + 1,
                                _AGGREGATE_ACTUAL_BYTES_LIMIT - actual_total + 1,
                            )
                            chunk = stream.read(read_size)

                            if not chunk:
                                break

                            actual_member += len(chunk)
                            actual_total += len(chunk)

                            if actual_member > _MEMBER_ACTUAL_BYTES_LIMIT:
                                raise ArtifactContentSnapshotError(
                                    f"wheel member {info.filename!r} exceeds "
                                    "per-member inspection limit"
                                )

                            if actual_total > _AGGREGATE_ACTUAL_BYTES_LIMIT:
                                raise ArtifactContentSnapshotError(
                                    "wheel exceeds aggregate decompressed "
                                    "inspection limit"
                                )

                            member_hasher.update(chunk)

                    members.append(
                        ArtifactContentMember(
                            path=name,
                            size=actual_member,
                            digest_algorithm=ArtifactDigestAlgorithm.SHA256,
                            digest=member_hasher.hexdigest(),
                        )
                    )
        except (OSError, zipfile.BadZipFile) as error:
            raise ArtifactContentSnapshotError(
                f"cannot inspect wheel {path}"
            ) from error

        return ArtifactContentSnapshot(
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            members=tuple(sorted(members, key=lambda member: member.path)),
        )

    def _snapshot_sdist(self, path: Path) -> ArtifactContentSnapshot:
        raw_members: list[tuple[str, int, str]] = []
        roots: set[str] = set()
        normalized_names: set[str] = set()

        try:
            with (
                path.open("rb") as raw_archive,
                gzip.GzipFile(fileobj=raw_archive, mode="rb") as decompressed,
                tarfile.open(
                    fileobj=cast(BinaryIO, decompressed),
                    mode="r|",
                    bufsize=_STREAM_CHUNK_BYTES,
                ) as archive,
            ):
                actual_total = 0

                for member_count, member in enumerate(archive, start=1):
                    if member_count > _ARCHIVE_MEMBER_COUNT_LIMIT:
                        raise ArtifactContentSnapshotError(
                            "source archive exceeds archive member inspection limit"
                        )

                    name = self._normalized_archive_member_name(member.name)
                    self._require_safe_path(name)

                    if name in normalized_names:
                        raise ArtifactContentSnapshotError(
                            "source archive contains duplicate normalized "
                            f"member path {name!r}"
                        )
                    normalized_names.add(name)

                    if not (member.isfile() or member.isdir()):
                        raise ArtifactContentSnapshotError(
                            f"source archive member {member.name!r} is not "
                            "a regular file or directory"
                        )

                    parts = PurePosixPath(name).parts
                    roots.add(parts[0])

                    if member.isdir():
                        continue

                    stream = archive.extractfile(member)
                    if stream is None:
                        raise ArtifactContentSnapshotError(
                            f"cannot read source archive member {member.name!r}"
                        )

                    member_hasher = hashlib.sha256()
                    actual_member = 0

                    while True:
                        chunk = stream.read(
                            min(
                                _STREAM_CHUNK_BYTES,
                                _MEMBER_ACTUAL_BYTES_LIMIT - actual_member + 1,
                            )
                        )

                        if not chunk:
                            break

                        actual_member += len(chunk)
                        actual_total += len(chunk)

                        if actual_member > _MEMBER_ACTUAL_BYTES_LIMIT:
                            raise ArtifactContentSnapshotError(
                                f"source archive member {member.name!r} "
                                "exceeds per-member inspection limit"
                            )

                        if actual_total > _AGGREGATE_ACTUAL_BYTES_LIMIT:
                            raise ArtifactContentSnapshotError(
                                "source archive exceeds aggregate "
                                "decompressed inspection limit"
                            )

                        member_hasher.update(chunk)

                    raw_members.append(
                        (
                            name,
                            actual_member,
                            member_hasher.hexdigest(),
                        )
                    )
        except (OSError, EOFError, gzip.BadGzipFile, tarfile.TarError) as error:
            raise ArtifactContentSnapshotError(
                f"cannot inspect source distribution {path}"
            ) from error

        if len(roots) != 1:
            raise ArtifactContentSnapshotError(
                "source archive must contain exactly one package root"
            )

        root = next(iter(roots))
        prefix = f"{root}/"

        members = []

        for name, size, member_digest in raw_members:
            if not name.startswith(prefix):
                raise ArtifactContentSnapshotError(
                    "source archive regular member is outside package root"
                )

            logical_path = name[len(prefix) :]

            self._require_safe_path(logical_path)

            members.append(
                ArtifactContentMember(
                    path=logical_path,
                    size=size,
                    digest_algorithm=ArtifactDigestAlgorithm.SHA256,
                    digest=member_digest,
                )
            )

        return ArtifactContentSnapshot(
            artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
            members=tuple(sorted(members, key=lambda member: member.path)),
        )

    def _normalized_archive_member_name(self, name: str) -> str:
        return name[:-1] if name.endswith("/") else name

    def _require_safe_path(self, name: str) -> None:
        if not name or "\x00" in name:
            raise ArtifactContentSnapshotError(
                "empty or NUL-containing archive member name"
            )

        if "\\" in name:
            raise ArtifactContentSnapshotError(
                "backslash-separated archive member name"
            )

        path = PurePosixPath(name)

        if path.is_absolute():
            raise ArtifactContentSnapshotError("absolute archive member name")

        parts = name.split("/")

        if any(part in {"", ".", ".."} for part in parts):
            raise ArtifactContentSnapshotError(
                "non-canonical or traversal-like archive member name"
            )

        if parts[0].endswith(":"):
            raise ArtifactContentSnapshotError("drive-qualified archive member name")

    def _require_safe_zip_type(self, member: zipfile.ZipInfo) -> None:
        if member.create_system != 3:
            return

        unix_mode = (member.external_attr >> 16) & 0xFFFF
        member_type = stat.S_IFMT(unix_mode)

        if member.is_dir():
            if member_type not in {0, stat.S_IFDIR}:
                raise ArtifactContentSnapshotError(
                    f"wheel member {member.filename!r} has unsupported "
                    "non-directory Unix file type"
                )
            return

        if member_type not in {0, stat.S_IFREG}:
            raise ArtifactContentSnapshotError(
                f"wheel member {member.filename!r} has unsupported "
                "non-regular Unix file type"
            )
