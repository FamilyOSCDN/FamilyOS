"""Tests for the canonical build workspace model."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.build.build_workspace import BuildWorkspace


def test_workspace_preserves_canonical_layout(tmp_path: Path) -> None:
    root = tmp_path.resolve() / "familyos-build" / "build-id"

    workspace = BuildWorkspace(
        root=root,
        staging_dir=root / "staging",
        intermediate_dir=root / "intermediate",
    )

    assert workspace.root == root
    assert workspace.staging_dir == root / "staging"
    assert workspace.intermediate_dir == root / "intermediate"


def test_workspace_requires_absolute_root() -> None:
    root = Path("relative-workspace")

    with pytest.raises(
        ValueError,
        match="workspace root must be absolute",
    ):
        BuildWorkspace(
            root=root,
            staging_dir=root / "staging",
            intermediate_dir=root / "intermediate",
        )


def test_workspace_rejects_noncanonical_staging_directory(
    tmp_path: Path,
) -> None:
    root = tmp_path.resolve() / "workspace"

    with pytest.raises(
        ValueError,
        match="workspace staging directory must be rooted at workspace root",
    ):
        BuildWorkspace(
            root=root,
            staging_dir=root / "other",
            intermediate_dir=root / "intermediate",
        )


def test_workspace_rejects_noncanonical_intermediate_directory(
    tmp_path: Path,
) -> None:
    root = tmp_path.resolve() / "workspace"

    with pytest.raises(
        ValueError,
        match="workspace intermediate directory must be rooted at workspace root",
    ):
        BuildWorkspace(
            root=root,
            staging_dir=root / "staging",
            intermediate_dir=root / "other",
        )


def test_workspace_is_immutable(tmp_path: Path) -> None:
    root = tmp_path.resolve() / "workspace"
    workspace = BuildWorkspace(
        root=root,
        staging_dir=root / "staging",
        intermediate_dir=root / "intermediate",
    )

    with pytest.raises(AttributeError):
        workspace.root = tmp_path / "replacement"  # type: ignore[misc]
