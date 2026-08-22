"""Tests for canonical dependency-input freshness validation."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.dependency_input_freshness import (
    DEPENDENCY_DIGEST_PREFIX,
    dependency_input_digest,
    validate_dependency_input_freshness,
)


def _write_dependency_pyproject(path: Path) -> None:
    path.write_text(
        "\n".join(
            (
                "[build-system]",
                'requires = ["setuptools>=75", "wheel"]',
                'build-backend = "setuptools.build_meta"',
                "",
                "[project]",
                'name = "familyos-cli"',
                'version = "0.1.0"',
                'requires-python = ">=3.13"',
                'dependencies = ["typer>=0.16"]',
                "",
                "[project.optional-dependencies]",
                'dev = ["pytest>=8.4", "pip-tools==7.6.1"]',
                "",
            )
        ),
        encoding="utf-8",
    )


def test_dependency_input_digest_is_deterministic(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"

    _write_dependency_pyproject(pyproject_path)

    first = dependency_input_digest(pyproject_path)
    second = dependency_input_digest(pyproject_path)

    assert first == second
    assert len(first) == 64


def test_matching_generated_dependency_digest_is_fresh(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    requirements_path = tmp_path / "requirements.txt"

    _write_dependency_pyproject(pyproject_path)

    digest = dependency_input_digest(pyproject_path)

    requirements_path.write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{digest}\n"
        "package==1.0\n",
        encoding="utf-8",
    )

    result = validate_dependency_input_freshness(
        pyproject_path=pyproject_path,
        requirements_path=requirements_path,
    )

    assert result.successful is True
    assert result.diagnostic is None


def test_missing_generated_dependency_digest_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    requirements_path = tmp_path / "requirements.txt"

    _write_dependency_pyproject(pyproject_path)

    requirements_path.write_text(
        "package==1.0\n",
        encoding="utf-8",
    )

    result = validate_dependency_input_freshness(
        pyproject_path=pyproject_path,
        requirements_path=requirements_path,
    )

    assert result.successful is False
    assert result.diagnostic == (
        "generated dependency input requirements.txt "
        "does not contain its canonical dependency digest"
    )


def test_stale_generated_dependency_digest_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    requirements_path = tmp_path / "requirements.txt"

    _write_dependency_pyproject(pyproject_path)

    requirements_path.write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{'0' * 64}\n"
        "package==1.0\n",
        encoding="utf-8",
    )

    result = validate_dependency_input_freshness(
        pyproject_path=pyproject_path,
        requirements_path=requirements_path,
    )

    assert result.successful is False
    assert result.diagnostic == (
        "generated dependency input requirements.txt is stale; "
        "regenerate requirements.txt"
    )


def test_missing_requirements_file_fails(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    requirements_path = tmp_path / "requirements.txt"

    _write_dependency_pyproject(pyproject_path)

    result = validate_dependency_input_freshness(
        pyproject_path=pyproject_path,
        requirements_path=requirements_path,
    )

    assert result.successful is False
    assert result.diagnostic is not None
    assert result.diagnostic.startswith(
        "unable to validate generated dependency input freshness:"
    )
