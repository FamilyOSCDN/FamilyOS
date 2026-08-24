"""Tests for canonical build workspace initialization."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_workspace_initializer import (
    BuildWorkspaceInitializer,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)


def test_initializer_creates_canonical_workspace_layout(
    tmp_path: Path,
) -> None:
    temporary_directory = tmp_path.resolve()

    workspace = BuildWorkspaceInitializer().initialize(
        build_id=_BUILD_ID,
        temporary_directory=temporary_directory,
    )

    expected_root = (
        temporary_directory
        / "familyos-build"
        / str(_BUILD_ID)
    )

    assert workspace.root == expected_root
    assert workspace.staging_dir == expected_root / "staging"
    assert workspace.intermediate_dir == expected_root / "intermediate"

    assert workspace.root.is_dir()
    assert workspace.staging_dir.is_dir()
    assert workspace.intermediate_dir.is_dir()


def test_initializer_isolates_workspaces_by_build_id(
    tmp_path: Path,
) -> None:
    first_id = BuildId(
        UUID("01234567-89ab-4cde-8f01-23456789abcd")
    )
    second_id = BuildId(
        UUID("11234567-89ab-4cde-8f01-23456789abcd")
    )
    initializer = BuildWorkspaceInitializer()

    first = initializer.initialize(
        build_id=first_id,
        temporary_directory=tmp_path,
    )
    second = initializer.initialize(
        build_id=second_id,
        temporary_directory=tmp_path,
    )

    assert first.root != second.root
    assert first.root.is_dir()
    assert second.root.is_dir()


def test_initializer_rejects_existing_build_workspace(
    tmp_path: Path,
) -> None:
    initializer = BuildWorkspaceInitializer()

    initializer.initialize(
        build_id=_BUILD_ID,
        temporary_directory=tmp_path,
    )

    with pytest.raises(FileExistsError):
        initializer.initialize(
            build_id=_BUILD_ID,
            temporary_directory=tmp_path,
        )
