from __future__ import annotations

import io
import tarfile
import zipfile
from pathlib import Path

import pytest

from familyos_cli.application.build.artifact_content_snapshotter import (
    ArtifactContentSnapshotError,
    ArtifactContentSnapshotter,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


def _write_wheel(
    path: Path,
    members: tuple[tuple[str, bytes], ...],
) -> None:
    with zipfile.ZipFile(
        path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        for name, content in members:
            archive.writestr(name, content)


def _write_sdist(
    path: Path,
    *,
    root: str,
    members: tuple[tuple[str, bytes], ...],
) -> None:
    with tarfile.open(path, mode="w:gz") as archive:
        for relative_path, content in members:
            info = tarfile.TarInfo(
                name=f"{root}/{relative_path}"
            )
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))


def test_equivalent_wheels_have_matching_content_snapshots(
    tmp_path: Path,
) -> None:
    first_path = tmp_path / "first.whl"
    second_path = tmp_path / "second.whl"

    members = (
        ("familyos_cli/__init__.py", b""),
        ("familyos_cli/example.py", b"value = 1\n"),
    )

    _write_wheel(first_path, members)
    _write_wheel(second_path, tuple(reversed(members)))

    snapshotter = ArtifactContentSnapshotter()

    first = snapshotter.snapshot(
        first_path,
        ArtifactClass.PYTHON_WHEEL,
    )
    second = snapshotter.snapshot(
        second_path,
        ArtifactClass.PYTHON_WHEEL,
    )

    assert first.matches(second)
    assert tuple(member.path for member in first.members) == (
        "familyos_cli/__init__.py",
        "familyos_cli/example.py",
    )


def test_changed_wheel_content_changes_snapshot(tmp_path: Path) -> None:
    first_path = tmp_path / "first.whl"
    second_path = tmp_path / "second.whl"

    _write_wheel(first_path, (("module.py", b"value = 1\n"),))
    _write_wheel(second_path, (("module.py", b"value = 2\n"),))

    snapshotter = ArtifactContentSnapshotter()

    first = snapshotter.snapshot(
        first_path,
        ArtifactClass.PYTHON_WHEEL,
    )
    second = snapshotter.snapshot(
        second_path,
        ArtifactClass.PYTHON_WHEEL,
    )

    assert not first.matches(second)


def test_equivalent_sdists_ignore_generated_archive_root(
    tmp_path: Path,
) -> None:
    first_path = tmp_path / "first.tar.gz"
    second_path = tmp_path / "second.tar.gz"

    members = (
        ("PKG-INFO", b"Name: familyos-cli\n"),
        ("src/familyos_cli/__init__.py", b""),
    )

    _write_sdist(
        first_path,
        root="familyos_cli-0.1.0",
        members=members,
    )
    _write_sdist(
        second_path,
        root="different-generated-root",
        members=tuple(reversed(members)),
    )

    snapshotter = ArtifactContentSnapshotter()

    first = snapshotter.snapshot(
        first_path,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )
    second = snapshotter.snapshot(
        second_path,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )

    assert first.matches(second)
    assert tuple(member.path for member in first.members) == (
        "PKG-INFO",
        "src/familyos_cli/__init__.py",
    )


def test_changed_sdist_content_changes_snapshot(tmp_path: Path) -> None:
    first_path = tmp_path / "first.tar.gz"
    second_path = tmp_path / "second.tar.gz"

    _write_sdist(
        first_path,
        root="package",
        members=(("module.py", b"value = 1\n"),),
    )
    _write_sdist(
        second_path,
        root="package",
        members=(("module.py", b"value = 2\n"),),
    )

    snapshotter = ArtifactContentSnapshotter()

    first = snapshotter.snapshot(
        first_path,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )
    second = snapshotter.snapshot(
        second_path,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )

    assert not first.matches(second)


@pytest.mark.parametrize(
    "name",
    (
        "../escape.py",
        "/absolute.py",
        r"pkg\module.py",
    ),
)
def test_wheel_rejects_unsafe_member_paths(
    tmp_path: Path,
    name: str,
) -> None:
    path = tmp_path / "unsafe.whl"
    _write_wheel(path, ((name, b"content"),))

    with pytest.raises(ArtifactContentSnapshotError):
        ArtifactContentSnapshotter().snapshot(
            path,
            ArtifactClass.PYTHON_WHEEL,
        )


def test_sdist_rejects_multiple_roots(tmp_path: Path) -> None:
    path = tmp_path / "multiple-roots.tar.gz"

    with tarfile.open(path, mode="w:gz") as archive:
        for name in ("first/a.py", "second/b.py"):
            content = b"content"
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))

    with pytest.raises(ArtifactContentSnapshotError):
        ArtifactContentSnapshotter().snapshot(
            path,
            ArtifactClass.SOURCE_DISTRIBUTION,
        )
