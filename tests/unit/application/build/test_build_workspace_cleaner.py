"""Tests for canonical build workspace failure cleanup."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.build_workspace_cleaner import (
    BuildWorkspaceCleaner,
)

from familyos_cli.application.build.build_workspace import BuildWorkspace


def _workspace(tmp_path: Path) -> BuildWorkspace:
    root = (tmp_path / "familyos-build" / "build-id").resolve()
    staging = root / "staging"
    intermediate = root / "intermediate"

    staging.mkdir(parents=True)
    intermediate.mkdir()

    return BuildWorkspace(
        root=root,
        staging_dir=staging,
        intermediate_dir=intermediate,
    )


def test_cleaner_removes_entire_build_workspace(
    tmp_path: Path,
) -> None:
    workspace = _workspace(tmp_path)

    staged_file = workspace.staging_dir / "project" / "package.txt"
    staged_file.parent.mkdir()
    staged_file.write_text("staged", encoding="utf-8")

    intermediate_file = workspace.intermediate_dir / "generated.txt"
    intermediate_file.write_text("intermediate", encoding="utf-8")

    BuildWorkspaceCleaner().clean(workspace=workspace)

    assert not workspace.root.exists()


def test_cleaner_is_idempotent_when_workspace_is_already_absent(
    tmp_path: Path,
) -> None:
    workspace = _workspace(tmp_path)
    workspace_root = workspace.root

    BuildWorkspaceCleaner().clean(workspace=workspace)
    BuildWorkspaceCleaner().clean(workspace=workspace)

    assert not workspace_root.exists()
