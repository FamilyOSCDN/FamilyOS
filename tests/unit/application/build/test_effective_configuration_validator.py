"""Tests for final effective build-configuration validation."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildEffectiveConfiguration,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_profile_definition import (
    BuildProfileDefinition,
)
from familyos_cli.application.build.build_profile_registry import (
    get_build_profile_definition,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.effective_configuration_validation import (
    EffectiveConfigurationValidationResult,
    EffectiveConfigurationValidationStatus,
)
from familyos_cli.application.build.effective_configuration_validator import (
    EffectiveConfigurationValidator,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.repository_layout_validation import (
    RepositoryLayoutValidationResult,
)
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)


def _context(
    tmp_path: Path,
    *,
    profile: BuildProfile = BuildProfile.DEVELOPMENT,
    functional_validation: object = False,
    evidence_output: Path | None = None,
) -> BuildContext:
    return BuildContext(
        build_id=BuildId(
            UUID("01234567-89ab-4cde-8f01-23456789abcd")
        ),
        source_state=SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
        dependency_state=DependencyState(
            declaration_path=tmp_path / "pyproject.toml",
            declaration_digest="a" * 64,
            lock_path=tmp_path / "requirements.txt",
            lock_digest="b" * 64,
        ),
        toolchain_state=ToolchainState(
            critical_versions=(ToolchainVersion("build", "1.5.0"),),
        ),
        environment_state=EnvironmentState(
            operating_system="TestOS",
            operating_system_release="1.0",
            machine_architecture="test-machine",
        ),
        profile=profile,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        runtime_version="3.13.7",
        effective_configuration=BuildEffectiveConfiguration(
            functional_validation=cast(bool, functional_validation),
        ),
        output_dir=tmp_path / "dist",
        evidence_output=evidence_output,
    )


def _validate(
    context: BuildContext,
    *,
    profile_definition: BuildProfileDefinition | None = None,
    output_layout_validation: RepositoryLayoutValidationResult | None = None,
    evidence_layout_validation: RepositoryLayoutValidationResult | None = None,
) -> EffectiveConfigurationValidationResult:
    return EffectiveConfigurationValidator().validate(
        context=context,
        profile_definition=(
            profile_definition
            or get_build_profile_definition(context.profile)
        ),
        output_layout_validation=(
            output_layout_validation
            or RepositoryLayoutValidationResult(successful=True)
        ),
        evidence_layout_validation=(
            evidence_layout_validation
            or RepositoryLayoutValidationResult(successful=True)
        ),
    )


def test_canonical_default_configuration_succeeds(tmp_path: Path) -> None:
    result = _validate(_context(tmp_path))

    assert result.status is EffectiveConfigurationValidationStatus.SUCCEEDED
    assert result.successful is True
    assert result.findings == ()


@pytest.mark.parametrize("profile", tuple(BuildProfile))
def test_supported_profile_target_succeeds(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    definition = get_build_profile_definition(profile)
    evidence_output = (
        tmp_path / "build-evidence.json"
        if definition.evidence_required
        else None
    )

    result = _validate(
        _context(
            tmp_path,
            profile=profile,
            evidence_output=evidence_output,
        )
    )

    assert result.successful is True


def test_inconsistent_profile_fails(tmp_path: Path) -> None:
    result = _validate(
        _context(tmp_path, profile=BuildProfile.CI),
        profile_definition=get_build_profile_definition(
            BuildProfile.DEVELOPMENT,
        ),
    )

    assert result.successful is False
    assert result.findings[0].component == "profile"
    assert result.findings[0].diagnostic == (
        "resolved build profile does not match canonical profile definition: "
        "context=ci, definition=development"
    )


def test_inconsistent_profile_target_fails(tmp_path: Path) -> None:
    definition = replace(
        get_build_profile_definition(BuildProfile.DEVELOPMENT),
        supported_targets=cast(
            tuple[BuildTarget, ...],
            ("unsupported-target",),
        ),
    )

    result = _validate(
        _context(tmp_path),
        profile_definition=definition,
    )

    assert result.successful is False
    assert result.findings[0].component == "target"
    assert result.findings[0].diagnostic == (
        "resolved build target is unsupported by profile: "
        "development/familyos-cli-package"
    )


@pytest.mark.parametrize("functional_validation", (False, True))
def test_boolean_functional_validation_state_is_accepted(
    tmp_path: Path,
    functional_validation: bool,
) -> None:
    context = _context(
        tmp_path,
        functional_validation=functional_validation,
    )

    result = _validate(context)

    assert result.successful is True
    assert (
        context.effective_configuration.functional_validation
        is functional_validation
    )


def test_non_boolean_functional_validation_state_fails(tmp_path: Path) -> None:
    result = _validate(
        _context(tmp_path, functional_validation="yes"),
    )

    assert result.successful is False
    assert result.findings[0].component == "functional-validation"
    assert result.findings[0].diagnostic == (
        "resolved functional-validation setting must be a boolean"
    )


def test_failed_repository_layout_decision_is_preserved(
    tmp_path: Path,
) -> None:
    result = _validate(
        _context(tmp_path),
        output_layout_validation=RepositoryLayoutValidationResult(
            successful=False,
            diagnostic="output conflicts with repository content",
        ),
    )

    assert result.successful is False
    assert result.findings[0].component == "output-directory"
    assert result.findings[0].diagnostic == (
        "output conflicts with repository content"
    )


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.DEVELOPMENT, BuildProfile.VALIDATION),
)
def test_profile_without_required_evidence_accepts_no_destination(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    result = _validate(_context(tmp_path, profile=profile))

    assert result.successful is True


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.CI, BuildProfile.RELEASE_CANDIDATE),
)
def test_profile_requiring_evidence_rejects_missing_destination(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    result = _validate(_context(tmp_path, profile=profile))

    assert result.successful is False
    assert result.findings[0].component == "evidence"
    assert result.findings[0].diagnostic == (
        f"build profile requires an evidence output: {profile.value}"
    )


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.CI, BuildProfile.RELEASE_CANDIDATE),
)
def test_profile_requiring_evidence_accepts_destination(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    context = _context(
        tmp_path,
        profile=profile,
        evidence_output=tmp_path / "build-evidence.json",
    )

    result = _validate(context)

    assert result.successful is True
    assert context.evidence_output == tmp_path / "build-evidence.json"


def test_failed_evidence_layout_decision_is_preserved(
    tmp_path: Path,
) -> None:
    result = _validate(
        _context(
            tmp_path,
            evidence_output=tmp_path / "pyproject.toml",
        ),
        evidence_layout_validation=RepositoryLayoutValidationResult(
            successful=False,
            diagnostic=(
                "build evidence output must not replace "
                "authoritative repository files"
            ),
        ),
    )

    assert result.successful is False
    assert result.findings[0].component == "evidence-output"
    assert result.findings[0].diagnostic == (
        "build evidence output must not replace "
        "authoritative repository files"
    )


def test_multiple_findings_have_deterministic_order(tmp_path: Path) -> None:
    definition = replace(
        get_build_profile_definition(BuildProfile.DEVELOPMENT),
        supported_targets=cast(
            tuple[BuildTarget, ...],
            ("unsupported-target",),
        ),
    )
    context = _context(
        tmp_path,
        profile=BuildProfile.CI,
        functional_validation="yes",
    )

    result = _validate(
        context,
        profile_definition=definition,
        output_layout_validation=RepositoryLayoutValidationResult(
            successful=False,
            diagnostic="output conflicts with repository content",
        ),
        evidence_layout_validation=RepositoryLayoutValidationResult(
            successful=False,
            diagnostic="evidence conflicts with repository content",
        ),
    )

    assert tuple(finding.component for finding in result.findings) == (
        "profile",
        "target",
        "functional-validation",
        "output-directory",
        "evidence-output",
    )
    assert result.diagnostic == (
        "resolved build profile does not match canonical profile definition: "
        "context=ci, definition=development; "
        "resolved build target is unsupported by profile: "
        "ci/familyos-cli-package; "
        "resolved functional-validation setting must be a boolean; "
        "output conflicts with repository content; "
        "evidence conflicts with repository content"
    )
