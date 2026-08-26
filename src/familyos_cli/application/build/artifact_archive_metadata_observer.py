"""Archive metadata observation for reproducibility analysis."""

from __future__ import annotations

import gzip
import stat
import tarfile
import zipfile
from pathlib import Path
from typing import Any, BinaryIO, cast

from familyos_cli.application.build.artifact_archive_metadata import (
    ArchiveMetadataField,
    ArtifactArchiveMetadataObservation,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


class ArtifactArchiveMetadataObservationError(ValueError):
    """Raised when archive metadata cannot be observed safely."""


class ArtifactArchiveMetadataObserver:
    """Observe canonical metadata variability between package artifacts."""

    def compare(
        self,
        left_path: Path,
        right_path: Path,
        artifact_type: ArtifactClass,
    ) -> ArtifactArchiveMetadataObservation:
        """Observe metadata differences between equivalent-build artifacts."""

        if artifact_type is ArtifactClass.PYTHON_WHEEL:
            differing_fields = self._compare_wheels(
                left_path,
                right_path,
            )
        elif artifact_type is ArtifactClass.SOURCE_DISTRIBUTION:
            differing_fields = self._compare_sdists(
                left_path,
                right_path,
            )
        else:
            raise ArtifactArchiveMetadataObservationError(
                f"unsupported artifact type: {artifact_type}"
            )

        return ArtifactArchiveMetadataObservation(
            artifact_type=artifact_type,
            differing_fields=tuple(
                sorted(differing_fields, key=lambda field: field.value)
            ),
        )

    def _compare_wheels(
        self,
        left_path: Path,
        right_path: Path,
    ) -> set[ArchiveMetadataField]:
        try:
            with (
                zipfile.ZipFile(left_path) as left_archive,
                zipfile.ZipFile(right_path) as right_archive,
            ):
                left = self._wheel_metadata(left_archive)
                right = self._wheel_metadata(right_archive)
        except (OSError, zipfile.BadZipFile) as error:
            raise ArtifactArchiveMetadataObservationError(
                "cannot inspect wheel metadata"
            ) from error

        return self._compare_member_metadata(left, right)

    def _wheel_metadata(
        self,
        archive: zipfile.ZipFile,
    ) -> dict[str, dict[ArchiveMetadataField, Any]]:
        result: dict[str, dict[ArchiveMetadataField, Any]] = {}

        for info in archive.infolist():
            name = self._normalized_name(info.filename)

            if name in result:
                raise ArtifactArchiveMetadataObservationError(
                    f"wheel contains duplicate member path {name!r}"
                )

            unix_mode = (
                (info.external_attr >> 16) & 0xFFFF if info.create_system == 3 else 0
            )

            result[name] = {
                ArchiveMetadataField.TIMESTAMP: info.date_time,
                ArchiveMetadataField.MODE: unix_mode,
                ArchiveMetadataField.SIZE: info.file_size,
                ArchiveMetadataField.TYPE: self._zip_member_type(
                    info,
                    unix_mode,
                ),
                ArchiveMetadataField.COMPRESSION: info.compress_type,
                ArchiveMetadataField.FLAGS: info.flag_bits,
            }

        return result

    def _compare_sdists(
        self,
        left_path: Path,
        right_path: Path,
    ) -> set[ArchiveMetadataField]:
        left = self._sdist_metadata(left_path)
        right = self._sdist_metadata(right_path)

        return self._compare_member_metadata(left, right)

    def _sdist_metadata(
        self,
        path: Path,
    ) -> dict[str, dict[ArchiveMetadataField, Any]]:
        result: dict[str, dict[ArchiveMetadataField, Any]] = {}

        try:
            with (
                path.open("rb") as raw_archive,
                gzip.GzipFile(
                    fileobj=raw_archive,
                    mode="rb",
                ) as decompressed,
                tarfile.open(
                    fileobj=cast(BinaryIO, decompressed),
                    mode="r|",
                ) as archive,
            ):
                for member in archive:
                    name = self._normalized_name(member.name)

                    if name in result:
                        raise ArtifactArchiveMetadataObservationError(
                            f"source archive contains duplicate member path {name!r}"
                        )

                    result[name] = {
                        ArchiveMetadataField.TIMESTAMP: member.mtime,
                        ArchiveMetadataField.MODE: member.mode,
                        ArchiveMetadataField.OWNER: member.uid,
                        ArchiveMetadataField.GROUP: member.gid,
                        ArchiveMetadataField.SIZE: member.size,
                        ArchiveMetadataField.TYPE: member.type,
                        ArchiveMetadataField.LINK: member.linkname,
                    }
        except (
            OSError,
            EOFError,
            gzip.BadGzipFile,
            tarfile.TarError,
        ) as error:
            raise ArtifactArchiveMetadataObservationError(
                f"cannot inspect source distribution metadata {path}"
            ) from error

        return result

    def _compare_member_metadata(
        self,
        left: dict[str, dict[ArchiveMetadataField, Any]],
        right: dict[str, dict[ArchiveMetadataField, Any]],
    ) -> set[ArchiveMetadataField]:
        differing_fields: set[ArchiveMetadataField] = set()

        if set(left) != set(right):
            differing_fields.add(ArchiveMetadataField.TYPE)

        for name in set(left) & set(right):
            left_metadata = left[name]
            right_metadata = right[name]

            fields = set(left_metadata) | set(right_metadata)

            for field in fields:
                if left_metadata.get(field) != right_metadata.get(field):
                    differing_fields.add(field)

        return differing_fields

    def _normalized_name(self, name: str) -> str:
        return name[:-1] if name.endswith("/") else name

    def _zip_member_type(
        self,
        info: zipfile.ZipInfo,
        unix_mode: int,
    ) -> str:
        if info.is_dir():
            return "directory"

        if info.create_system != 3:
            return "file"

        member_type = stat.S_IFMT(unix_mode)

        if member_type in {0, stat.S_IFREG}:
            return "file"

        if member_type == stat.S_IFDIR:
            return "directory"

        return f"unsupported:{member_type}"
