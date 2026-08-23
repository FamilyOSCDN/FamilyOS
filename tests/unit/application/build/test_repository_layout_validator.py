"""Tests for canonical repository-layout validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.build.repository_layout import RepositoryLayout
from familyos_cli.application.build.repository_layout_validation import (
    RepositoryLayoutValidationResult,
)
from familyos_cli.application.build.repository_layout_validator import (
    RepositoryLayoutValidator,
)


def _validate(
    project_root: Path,
    output_dir: Path,
) -> RepositoryLayoutValidationResult:
    return RepositoryLayoutValidator().validate_output_dir(
        layout=RepositoryLayout.from_project_root(project_root),
        output_dir=output_dir,
    )


@pytest.mark.parametrize(
    "output_dir",
    (
        Path("dist"),
        Path("dist/packages"),
        Path("build-output"),
        Path("artifacts/packages"),
        Path("generated/package-output"),
    ),
)
def test_safe_relative_output_directories_are_accepted(
    tmp_path: Path,
    output_dir: Path,
) -> None:
    result = _validate(
        tmp_path,
        output_dir,
    )

    assert result.successful is True
    assert result.diagnostic is None


def test_safe_absolute_output_outside_repository_is_accepted(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "external-artifacts"

    result = _validate(
        project_root,
        output_dir,
    )

    assert result.successful is True
    assert result.diagnostic is None


def test_repository_root_is_rejected(
    tmp_path: Path,
) -> None:
    result = _validate(
        tmp_path,
        tmp_path,
    )

    assert result.successful is False
    assert result.diagnostic == (
        "build output directory must not be the repository root"
    )


@pytest.mark.parametrize(
    "output_dir",
    (
        Path("src"),
        Path("src/generated"),
        Path("src/familyos_cli/dist"),
        Path("tests"),
        Path("tests/build-output"),
        Path("docs"),
        Path("docs/generated"),
        Path("scripts"),
        Path("scripts/output"),
        Path(".github"),
        Path(".github/artifacts"),
        Path("specifications"),
        Path("specifications/generated"),
        Path("templates"),
        Path("templates/packages"),
    ),
)
def test_authoritative_directories_are_rejected(
    tmp_path: Path,
    output_dir: Path,
) -> None:
    result = _validate(
        tmp_path,
        output_dir,
    )

    assert result.successful is False
    assert result.diagnostic == (
        "build output directory must not overlap "
        "authoritative repository content"
    )


@pytest.mark.parametrize(
    "output_dir",
    (
        Path("pyproject.toml"),
        Path("requirements.txt"),
    ),
)
def test_authoritative_files_are_rejected_as_output_locations(
    tmp_path: Path,
    output_dir: Path,
) -> None:
    result = _validate(
        tmp_path,
        output_dir,
    )

    assert result.successful is False
    assert result.diagnostic == (
        "build output directory must not replace "
        "authoritative repository files"
    )


def test_relative_output_is_resolved_from_project_root(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"

    relative_result = _validate(
        project_root,
        Path("dist"),
    )
    absolute_result = _validate(
        project_root,
        project_root / "dist",
    )

    assert relative_result == absolute_result
