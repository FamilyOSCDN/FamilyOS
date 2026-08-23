"""Tests for the canonical immutable Build Context."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildEffectiveConfiguration,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)

_DEPENDENCY_STATE = DependencyState(
    declaration_path=Path("/project/pyproject.toml"),
    declaration_digest="a" * 64,
    lock_path=Path("/project/requirements.txt"),
    lock_digest="b" * 64,
)

_TOOLCHAIN_STATE = ToolchainState(
    critical_versions=(
        ToolchainVersion("build", "1.5.0"),
        ToolchainVersion("pip-tools", "7.6.1"),
        ToolchainVersion("setuptools", "84.0.0"),
        ToolchainVersion("wheel", "0.48.0"),
    ),
)

_ENVIRONMENT_STATE = EnvironmentState(
    operating_system="Darwin",
    operating_system_release="24.6.0",
    machine_architecture="arm64",
)


def _context() -> BuildContext:
    return BuildContext(
        build_id=_BUILD_ID,
        source_state=_SOURCE_STATE,
        dependency_state=_DEPENDENCY_STATE,
        toolchain_state=_TOOLCHAIN_STATE,
        environment_state=_ENVIRONMENT_STATE,
        profile=BuildProfile.VALIDATION,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        runtime_version="3.13.7",
        effective_configuration=BuildEffectiveConfiguration(
            functional_validation=True,
        ),
        output_dir=Path("/tmp/familyos-dist"),
    )


def test_context_captures_minimum_effective_build_state() -> None:
    context = _context()

    assert context.build_id == _BUILD_ID
    assert context.source_state is _SOURCE_STATE
    assert context.source_state.revision == _SOURCE_STATE.revision
    assert context.source_state.dirty is False
    assert context.dependency_state is _DEPENDENCY_STATE
    assert context.toolchain_state is _TOOLCHAIN_STATE
    assert context.environment_state is _ENVIRONMENT_STATE
    assert context.environment_state.operating_system == "Darwin"
    assert context.environment_state.operating_system_release == "24.6.0"
    assert context.environment_state.machine_architecture == "arm64"
    assert context.profile is BuildProfile.VALIDATION
    assert context.target is BuildTarget.FAMILYOS_CLI_PACKAGE
    assert context.runtime_version == "3.13.7"
    assert context.effective_configuration.functional_validation is True
    assert context.output_dir == Path("/tmp/familyos-dist")
    assert context.evidence_output is None


def test_build_profiles_are_explicit() -> None:
    assert tuple(BuildProfile) == (
        BuildProfile.DEVELOPMENT,
        BuildProfile.VALIDATION,
        BuildProfile.CI,
        BuildProfile.RELEASE_CANDIDATE,
    )


def test_initial_build_target_is_explicit() -> None:
    assert tuple(BuildTarget) == (
        BuildTarget.FAMILYOS_CLI_PACKAGE,
    )


def test_context_is_immutable_after_resolution() -> None:
    context = _context()

    with pytest.raises(FrozenInstanceError):
        context.runtime_version = "3.14.0"  # type: ignore[misc]


def test_build_id_is_immutable_with_context() -> None:
    context = _context()

    with pytest.raises(FrozenInstanceError):
        context.build_id = BuildId(  # type: ignore[misc]
            UUID("fedcba98-7654-4321-8abc-def012345678")
        )


def test_environment_state_is_immutable_after_resolution() -> None:
    context = _context()

    with pytest.raises(FrozenInstanceError):
        context.environment_state.operating_system = "Linux"  # type: ignore[misc]


def test_effective_configuration_is_immutable() -> None:
    configuration = BuildEffectiveConfiguration(
        functional_validation=False,
    )

    with pytest.raises(FrozenInstanceError):
        configuration.functional_validation = True  # type: ignore[misc]
