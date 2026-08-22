"""Tests for canonical build input validation."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.build_context import BuildTarget
from familyos_cli.application.build.build_input_validator import (
    BuildInputValidator,
)
from familyos_cli.application.build.build_target_registry import (
    get_build_target_definition,
)


def test_valid_project_inputs_pass(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[build-system]\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = BuildInputValidator().validate(
        project_root=tmp_path,
        target_definition=get_build_target_definition(
            BuildTarget.FAMILYOS_CLI_PACKAGE,
        ),
    )

    assert result.successful is True
    assert result.diagnostic is None


def test_missing_pyproject_fails(
    tmp_path: Path,
) -> None:
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = BuildInputValidator().validate(
        project_root=tmp_path,
        target_definition=get_build_target_definition(
            BuildTarget.FAMILYOS_CLI_PACKAGE,
        ),
    )

    assert result.successful is False
    assert result.diagnostic == (
        "required build input missing: pyproject.toml"
    )


def test_missing_requirements_fails(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[build-system]\n",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = BuildInputValidator().validate(
        project_root=tmp_path,
        target_definition=get_build_target_definition(
            BuildTarget.FAMILYOS_CLI_PACKAGE,
        ),
    )

    assert result.successful is False
    assert result.diagnostic == (
        "required build input missing: requirements.txt"
    )


def test_missing_package_source_fails(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        "[build-system]\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )

    result = BuildInputValidator().validate(
        project_root=tmp_path,
        target_definition=get_build_target_definition(
            BuildTarget.FAMILYOS_CLI_PACKAGE,
        ),
    )

    assert result.successful is False
    assert result.diagnostic == (
        "required build input missing: "
        "package source governed by pyproject.toml"
    )
