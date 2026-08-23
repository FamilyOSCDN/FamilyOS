"""Tests for canonical build input validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.build.build_context import BuildTarget
from familyos_cli.application.build.build_input_validation import (
    BuildInputValidationResult,
)
from familyos_cli.application.build.build_input_validator import (
    BuildInputValidator,
)
from familyos_cli.application.build.build_target_registry import (
    get_build_target_definition,
)
from familyos_cli.application.build.dependency_input_freshness import (
    DEPENDENCY_DIGEST_PREFIX,
    dependency_input_digest,
)

_VALID_PYPROJECT = """\
[build-system]
requires = ["setuptools>=75", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "familyos-cli"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["typer>=0.16"]

[project.optional-dependencies]
dev = ["pytest>=8.4", "pip-tools==7.6.1"]
"""


def _write_required_inputs(
    project_root: Path,
    *,
    pyproject: str = _VALID_PYPROJECT,
    fresh_lock: bool = True,
) -> None:
    pyproject_path = project_root / "pyproject.toml"
    requirements_path = project_root / "requirements.txt"

    pyproject_path.write_text(
        pyproject,
        encoding="utf-8",
    )

    if fresh_lock:
        digest = dependency_input_digest(pyproject_path)
        requirements_path.write_text(
            f"{DEPENDENCY_DIGEST_PREFIX}{digest}\n"
            "package==1.0\n",
            encoding="utf-8",
        )
    else:
        requirements_path.write_text(
            "package==1.0\n",
            encoding="utf-8",
        )

    (project_root / "src").mkdir()


def _validate(
    project_root: Path,
) -> BuildInputValidationResult:
    return BuildInputValidator().validate(
        project_root=project_root,
        target_definition=get_build_target_definition(
            BuildTarget.FAMILYOS_CLI_PACKAGE,
        ),
    )


def test_valid_project_inputs_pass(
    tmp_path: Path,
) -> None:
    _write_required_inputs(tmp_path)

    result = _validate(tmp_path)

    assert result.successful is True
    assert result.diagnostic is None
    assert result.checks[-2].input_name == "package metadata"
    assert result.checks[-2].successful is True
    assert (
        result.checks[-1].input_name
        == "generated dependency input freshness"
    )
    assert result.checks[-1].successful is True


def test_missing_pyproject_fails(
    tmp_path: Path,
) -> None:
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "required build input missing: pyproject.toml"
    )


def test_missing_requirements_fails(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        _VALID_PYPROJECT,
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "required build input missing: requirements.txt"
    )


def test_missing_package_source_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    requirements_path = tmp_path / "requirements.txt"

    pyproject_path.write_text(
        _VALID_PYPROJECT,
        encoding="utf-8",
    )

    digest = dependency_input_digest(pyproject_path)
    requirements_path.write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{digest}\n",
        encoding="utf-8",
    )

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "required build input missing: "
        "package source governed by pyproject.toml"
    )


def test_malformed_pyproject_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_path.write_text(
        "[project\nname = broken\n",
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "build metadata pyproject.toml is malformed"
    )


def test_missing_project_table_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_path.write_text(
        "[build-system]\n"
        'requires = ["setuptools>=75", "wheel"]\n'
        'build-backend = "setuptools.build_meta"\n',
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "build metadata pyproject.toml does not contain "
        "a valid [project] table"
    )


@pytest.mark.parametrize(
    ("pyproject", "diagnostic"),
    (
        (
            (
                "[project]\n"
                'version = "0.1.0"\n'
                'requires-python = ">=3.13"\n'
            ),
            (
                "build metadata pyproject.toml "
                "project.name is missing or invalid"
            ),
        ),
        (
            (
                "[project]\n"
                'name = "familyos-cli"\n'
                'requires-python = ">=3.13"\n'
            ),
            (
                "build metadata pyproject.toml "
                "project.version is missing or invalid"
            ),
        ),
        (
            (
                "[project]\n"
                'name = "familyos-cli"\n'
                'version = "0.1.0"\n'
            ),
            (
                "build metadata pyproject.toml "
                "project.requires-python is missing or invalid"
            ),
        ),
    ),
)
def test_missing_required_package_metadata_fails(
    tmp_path: Path,
    pyproject: str,
    diagnostic: str,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_path.write_text(
        pyproject,
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == diagnostic


def test_empty_package_name_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"

    pyproject_path.write_text(
        "[project]\n"
        'name = "   "\n'
        'version = "0.1.0"\n'
        'requires-python = ">=3.13"\n',
        encoding="utf-8",
    )
    (tmp_path / "requirements.txt").write_text(
        "",
        encoding="utf-8",
    )
    (tmp_path / "src").mkdir()

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "build metadata pyproject.toml "
        "project.name is missing or invalid"
    )


def test_missing_dependency_digest_fails(
    tmp_path: Path,
) -> None:
    _write_required_inputs(
        tmp_path,
        fresh_lock=False,
    )

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "generated dependency input requirements.txt "
        "does not contain its canonical dependency digest"
    )


def test_stale_generated_dependency_input_fails(
    tmp_path: Path,
) -> None:
    _write_required_inputs(tmp_path)

    requirements_path = tmp_path / "requirements.txt"
    requirements_path.write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{'0' * 64}\n"
        "package==1.0\n",
        encoding="utf-8",
    )

    result = _validate(tmp_path)

    assert result.successful is False
    assert result.diagnostic == (
        "generated dependency input requirements.txt is stale; "
        "regenerate requirements.txt"
    )
