"""Tests for canonical build-toolchain policy resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.build.toolchain_policy_provider import (
    ToolchainPolicyProvider,
)


def _write_pyproject(
    project_root: Path,
    *,
    requires_python: str = ">=3.13",
    mypy_python: str = "3.13",
    build_requirement: str = "build>=1.5",
    pip_tools_requirement: str = "pip-tools==7.6.1",
    setuptools_requirement: str = "setuptools>=75",
    wheel_requirement: str = "wheel",
) -> None:
    project_root.mkdir(parents=True, exist_ok=True)

    (project_root / "pyproject.toml").write_text(
        "[build-system]\n"
        "requires = [\n"
        f'    "{setuptools_requirement}",\n'
        f'    "{wheel_requirement}",\n'
        "]\n"
        'build-backend = "setuptools.build_meta"\n'
        "\n"
        "[project]\n"
        'name = "familyos-test"\n'
        'version = "0.0.0"\n'
        f'requires-python = "{requires_python}"\n'
        "\n"
        "[project.optional-dependencies]\n"
        "dev = [\n"
        f'    "{build_requirement}",\n'
        f'    "{pip_tools_requirement}",\n'
        '    "ruff>=0.12",\n'
        '    "mypy>=1.17",\n'
        '    "pytest>=8.4",\n'
        "]\n"
        "\n"
        "[tool.mypy]\n"
        f'python_version = "{mypy_python}"\n',
        encoding="utf-8",
    )


def test_provider_resolves_canonical_toolchain_policy(
    tmp_path: Path,
) -> None:
    _write_pyproject(tmp_path)

    policy = ToolchainPolicyProvider().resolve(
        project_root=tmp_path,
    )

    assert policy.runtime_requirement == ">=3.13,<3.14"
    assert policy.requirements_by_distribution == {
        "build": ">=1.5",
        "pip-tools": "==7.6.1",
        "setuptools": ">=75",
        "wheel": "",
    }


def test_provider_preserves_declared_compatibility_constraints(
    tmp_path: Path,
) -> None:
    _write_pyproject(
        tmp_path,
        build_requirement="build>=1.6,<2",
        setuptools_requirement="setuptools>=80,<90",
        wheel_requirement="wheel>=0.45",
    )

    policy = ToolchainPolicyProvider().resolve(
        project_root=tmp_path,
    )

    assert policy.requirements_by_distribution == {
        "build": "<2,>=1.6",
        "pip-tools": "==7.6.1",
        "setuptools": "<90,>=80",
        "wheel": ">=0.45",
    }


def test_provider_rejects_missing_pyproject(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="canonical toolchain policy requires valid pyproject.toml",
    ):
        ToolchainPolicyProvider().resolve(
            project_root=tmp_path,
        )


def test_provider_rejects_invalid_canonical_runtime(
    tmp_path: Path,
) -> None:
    _write_pyproject(
        tmp_path,
        mypy_python="not-a-version",
    )

    with pytest.raises(
        ValueError,
        match="tool.mypy.python_version is invalid",
    ):
        ToolchainPolicyProvider().resolve(
            project_root=tmp_path,
        )


def test_provider_rejects_patch_specific_canonical_runtime(
    tmp_path: Path,
) -> None:
    _write_pyproject(
        tmp_path,
        mypy_python="3.13.1",
    )

    with pytest.raises(
        ValueError,
        match="canonical build runtime must identify a Python minor version",
    ):
        ToolchainPolicyProvider().resolve(
            project_root=tmp_path,
        )


def test_provider_rejects_runtime_outside_package_compatibility(
    tmp_path: Path,
) -> None:
    _write_pyproject(
        tmp_path,
        requires_python=">=3.14",
        mypy_python="3.13",
    )

    with pytest.raises(
        ValueError,
        match=(
            "canonical build runtime does not satisfy "
            "project.requires-python"
        ),
    ):
        ToolchainPolicyProvider().resolve(
            project_root=tmp_path,
        )


@pytest.mark.parametrize(
    ("distribution", "replacement"),
    (
        ("build", "other-build>=1"),
        ("pip-tools", "other-generator>=1"),
        ("setuptools", "other-backend>=1"),
        ("wheel", "other-wheel>=1"),
    ),
)
def test_provider_rejects_missing_critical_declaration(
    tmp_path: Path,
    distribution: str,
    replacement: str,
) -> None:
    arguments = {
        "build_requirement": "build>=1.5",
        "pip_tools_requirement": "pip-tools==7.6.1",
        "setuptools_requirement": "setuptools>=75",
        "wheel_requirement": "wheel",
    }

    key_by_distribution = {
        "build": "build_requirement",
        "pip-tools": "pip_tools_requirement",
        "setuptools": "setuptools_requirement",
        "wheel": "wheel_requirement",
    }

    arguments[key_by_distribution[distribution]] = replacement

    _write_pyproject(
        tmp_path,
        **arguments,
    )

    with pytest.raises(
        ValueError,
        match=(
            "required canonical toolchain declaration "
            f"'{distribution}' is missing"
        ),
    ):
        ToolchainPolicyProvider().resolve(
            project_root=tmp_path,
        )
