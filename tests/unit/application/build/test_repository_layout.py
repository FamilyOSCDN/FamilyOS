"""Tests for the canonical Build Framework repository layout."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from familyos_cli.application.build.repository_layout import RepositoryLayout


def test_layout_is_derived_from_project_root(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    assert layout.project_root == tmp_path
    assert layout.source_dir == tmp_path / "src"
    assert layout.tests_dir == tmp_path / "tests"
    assert layout.documentation_dir == tmp_path / "docs"
    assert layout.scripts_dir == tmp_path / "scripts"
    assert layout.automation_dir == tmp_path / ".github"
    assert layout.specifications_dir == tmp_path / "specifications"
    assert layout.templates_dir == tmp_path / "templates"
    assert layout.project_configuration == tmp_path / "pyproject.toml"
    assert layout.dependency_lock == tmp_path / "requirements.txt"
    assert layout.default_output_dir == tmp_path / "dist"
    assert layout.default_build_dir == tmp_path / "build"
    assert layout.generated_dir == tmp_path / "generated"


def test_authoritative_directories_are_explicit(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    assert layout.authoritative_directories == (
        tmp_path / "src",
        tmp_path / "tests",
        tmp_path / "docs",
        tmp_path / "scripts",
        tmp_path / ".github",
        tmp_path / "specifications",
        tmp_path / "templates",
    )


def test_authoritative_files_are_explicit(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    assert layout.authoritative_files == (
        tmp_path / "pyproject.toml",
        tmp_path / "requirements.txt",
    )


def test_authoritative_paths_combine_directories_and_files(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    assert layout.authoritative_paths == (
        tmp_path / "src",
        tmp_path / "tests",
        tmp_path / "docs",
        tmp_path / "scripts",
        tmp_path / ".github",
        tmp_path / "specifications",
        tmp_path / "templates",
        tmp_path / "pyproject.toml",
        tmp_path / "requirements.txt",
    )


def test_derived_directories_are_explicit(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    assert layout.derived_directories == (
        tmp_path / "dist",
        tmp_path / "build",
        tmp_path / "generated",
    )


def test_layout_is_immutable(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    with pytest.raises(FrozenInstanceError):
        layout.source_dir = tmp_path / "other"  # type: ignore[misc]


def test_layout_contains_no_developer_specific_absolute_paths(
    tmp_path: Path,
) -> None:
    layout = RepositoryLayout.from_project_root(tmp_path)

    expected_paths = (
        *layout.authoritative_paths,
        *layout.derived_directories,
    )

    for repository_path in expected_paths:
        assert repository_path.is_relative_to(layout.project_root)
