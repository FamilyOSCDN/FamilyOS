from __future__ import annotations

import io
import tarfile
import zipfile
from pathlib import Path

from familyos_cli.application.build.artifact_archive_metadata import (
    ArchiveMetadataField,
)
from familyos_cli.application.build.artifact_archive_metadata_observer import (
    ArtifactArchiveMetadataObserver,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


def _write_wheel(
    path: Path,
    *,
    timestamp: tuple[int, int, int, int, int, int],
) -> None:
    info = zipfile.ZipInfo(
        "familyos_cli/module.py",
        date_time=timestamp,
    )
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED

    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(info, b"value = 1\n")


def _write_sdist(
    path: Path,
    *,
    mtime: int,
) -> None:
    payload = b"value = 1\n"

    with tarfile.open(path, "w:gz") as archive:
        directory = tarfile.TarInfo("package-1.0")
        directory.type = tarfile.DIRTYPE
        directory.mode = 0o755
        directory.mtime = mtime
        archive.addfile(directory)

        member = tarfile.TarInfo("package-1.0/module.py")
        member.size = len(payload)
        member.mode = 0o644
        member.mtime = mtime
        archive.addfile(member, io.BytesIO(payload))


def test_identical_wheel_metadata_has_no_differences(
    tmp_path: Path,
) -> None:
    left = tmp_path / "left.whl"
    right = tmp_path / "right.whl"

    timestamp = (2026, 8, 26, 12, 0, 0)

    _write_wheel(left, timestamp=timestamp)
    _write_wheel(right, timestamp=timestamp)

    observation = ArtifactArchiveMetadataObserver().compare(
        left,
        right,
        ArtifactClass.PYTHON_WHEEL,
    )

    assert observation.differing_fields == ()
    assert observation.metadata_equal


def test_wheel_timestamp_variability_is_observed(
    tmp_path: Path,
) -> None:
    left = tmp_path / "left.whl"
    right = tmp_path / "right.whl"

    _write_wheel(
        left,
        timestamp=(2026, 8, 26, 12, 0, 0),
    )
    _write_wheel(
        right,
        timestamp=(2026, 8, 26, 12, 0, 2),
    )

    observation = ArtifactArchiveMetadataObserver().compare(
        left,
        right,
        ArtifactClass.PYTHON_WHEEL,
    )

    assert observation.differing_fields == (ArchiveMetadataField.TIMESTAMP,)


def test_identical_sdist_metadata_has_no_differences(
    tmp_path: Path,
) -> None:
    left = tmp_path / "left.tar.gz"
    right = tmp_path / "right.tar.gz"

    _write_sdist(left, mtime=1_700_000_000)
    _write_sdist(right, mtime=1_700_000_000)

    observation = ArtifactArchiveMetadataObserver().compare(
        left,
        right,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )

    assert observation.differing_fields == ()


def test_sdist_timestamp_variability_is_observed(
    tmp_path: Path,
) -> None:
    left = tmp_path / "left.tar.gz"
    right = tmp_path / "right.tar.gz"

    _write_sdist(left, mtime=1_700_000_000)
    _write_sdist(right, mtime=1_700_000_001)

    observation = ArtifactArchiveMetadataObserver().compare(
        left,
        right,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )

    assert observation.differing_fields == (ArchiveMetadataField.TIMESTAMP,)


def test_metadata_fields_are_reported_in_canonical_order(
    tmp_path: Path,
) -> None:
    left = tmp_path / "left.tar.gz"
    right = tmp_path / "right.tar.gz"

    payload = b"value = 1\n"

    with tarfile.open(left, "w:gz") as archive:
        member = tarfile.TarInfo("package-1.0/module.py")
        member.size = len(payload)
        member.mode = 0o644
        member.uid = 100
        member.mtime = 1_700_000_000
        archive.addfile(member, io.BytesIO(payload))

    with tarfile.open(right, "w:gz") as archive:
        member = tarfile.TarInfo("package-1.0/module.py")
        member.size = len(payload)
        member.mode = 0o600
        member.uid = 200
        member.mtime = 1_700_000_001
        archive.addfile(member, io.BytesIO(payload))

    observation = ArtifactArchiveMetadataObserver().compare(
        left,
        right,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )

    assert observation.differing_fields == tuple(
        sorted(
            (
                ArchiveMetadataField.MODE,
                ArchiveMetadataField.OWNER,
                ArchiveMetadataField.TIMESTAMP,
            ),
            key=lambda field: field.value,
        )
    )
