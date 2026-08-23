"""Tests for canonical build-toolchain compatibility validation."""

from __future__ import annotations

from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)
from familyos_cli.application.build.toolchain_validation import (
    ToolchainValidationStatus,
)
from familyos_cli.application.build.toolchain_validator import (
    ToolchainValidator,
)


def _state(
    *,
    build: str = "1.5.0",
    pip_tools: str = "7.6.1",
    setuptools: str = "84.0.0",
    wheel: str = "0.48.0",
) -> ToolchainState:
    return ToolchainState(
        critical_versions=(
            ToolchainVersion("build", build),
            ToolchainVersion("pip-tools", pip_tools),
            ToolchainVersion("setuptools", setuptools),
            ToolchainVersion("wheel", wheel),
        ),
    )


_REQUIREMENTS = {
    "build": ">=1.5",
    "pip-tools": "==7.6.1",
    "setuptools": ">=75",
    "wheel": "",
}


def test_compatible_toolchain_passes() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.13.7",
        toolchain_state=_state(),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert result.status is ToolchainValidationStatus.SUCCEEDED
    assert result.successful is True
    assert result.findings == ()
    assert result.diagnostic is None


def test_unsupported_runtime_fails() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.14.0",
        toolchain_state=_state(),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert result.successful is False
    assert result.findings[0].component == "python"
    assert result.findings[0].diagnostic == (
        "python 3.14.0 does not satisfy <3.14,>=3.13"
    )


def test_unsupported_build_version_fails() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.13.7",
        toolchain_state=_state(build="1.4.9"),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert result.successful is False
    assert result.findings[0].component == "build"
    assert result.findings[0].diagnostic == (
        "build 1.4.9 does not satisfy >=1.5"
    )


def test_pip_tools_exact_version_is_enforced() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.13.7",
        toolchain_state=_state(pip_tools="7.6.2"),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert result.successful is False
    assert result.findings[0].component == "pip-tools"
    assert result.findings[0].diagnostic == (
        "pip-tools 7.6.2 does not satisfy ==7.6.1"
    )


def test_missing_required_distribution_fails() -> None:
    state = ToolchainState(
        critical_versions=(
            ToolchainVersion("build", "1.5.0"),
            ToolchainVersion("setuptools", "84.0.0"),
            ToolchainVersion("wheel", "0.48.0"),
        ),
    )

    result = ToolchainValidator().validate(
        runtime_version="3.13.7",
        toolchain_state=state,
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert result.successful is False
    assert result.findings[0].component == "pip-tools"
    assert result.findings[0].diagnostic == (
        "required toolchain distribution 'pip-tools' is unavailable"
    )


def test_invalid_observed_version_fails() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.13.7",
        toolchain_state=_state(build="not-a-version"),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert result.successful is False
    assert result.findings[0].component == "build"
    assert result.findings[0].diagnostic == (
        "build version 'not-a-version' is invalid"
    )


def test_invalid_requirement_fails() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.13.7",
        toolchain_state=_state(),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements={
            "build": "not-a-specifier",
        },
    )

    assert result.successful is False
    assert result.findings[0].component == "build"
    assert result.findings[0].diagnostic == (
        "build requirement 'not-a-specifier' is invalid"
    )


def test_multiple_incompatibilities_are_reported_deterministically() -> None:
    result = ToolchainValidator().validate(
        runtime_version="3.14.0",
        toolchain_state=_state(
            build="1.4.0",
            pip_tools="7.6.2",
        ),
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=_REQUIREMENTS,
    )

    assert tuple(
        finding.component
        for finding in result.findings
    ) == (
        "python",
        "build",
        "pip-tools",
    )

    assert result.diagnostic == (
        "python 3.14.0 does not satisfy <3.14,>=3.13; "
        "build 1.4.0 does not satisfy >=1.5; "
        "pip-tools 7.6.2 does not satisfy ==7.6.1"
    )
