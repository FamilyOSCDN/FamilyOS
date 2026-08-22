"""Tests for canonical Build Profile definitions."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_profile_definition import (
    BuildProfileDefinition,
)
from familyos_cli.application.build.build_profile_registry import (
    get_build_profile_definition,
    validate_profile_target,
)


def test_all_canonical_profiles_have_definitions() -> None:
    definitions = tuple(
        get_build_profile_definition(profile)
        for profile in BuildProfile
    )

    assert tuple(definition.profile for definition in definitions) == (
        BuildProfile.DEVELOPMENT,
        BuildProfile.VALIDATION,
        BuildProfile.CI,
        BuildProfile.RELEASE_CANDIDATE,
    )


def test_development_profile_prioritizes_local_engineering() -> None:
    definition = get_build_profile_definition(
        BuildProfile.DEVELOPMENT,
    )

    assert "everyday local engineering" in definition.purpose
    assert definition.evidence_required is False
    assert BuildTarget.FAMILYOS_CLI_PACKAGE in definition.supported_targets
    assert "basic build execution" in definition.validation_scope
    assert "practical local isolation" in definition.environment_requirements


def test_validation_profile_captures_engineering_verification() -> None:
    definition = get_build_profile_definition(
        BuildProfile.VALIDATION,
    )

    assert "engineering state" in definition.purpose
    assert definition.validation_scope == (
        "ruff",
        "mypy",
        "pytest",
        "packaging checks",
        "structural checks",
    )
    assert definition.evidence_required is False


def test_ci_profile_requires_canonical_evidence() -> None:
    definition = get_build_profile_definition(BuildProfile.CI)

    assert definition.evidence_required is True
    assert "fresh environment" in definition.environment_requirements
    assert "evidence generation" in definition.validation_scope
    assert "build evidence" in definition.artifact_expectations


def test_release_candidate_profile_is_strongest_current_profile() -> None:
    definition = get_build_profile_definition(
        BuildProfile.RELEASE_CANDIDATE,
    )

    assert "strongest current" in definition.purpose
    assert definition.evidence_required is True
    assert "clean workspace" in definition.environment_requirements
    assert "release readiness" in definition.validation_scope
    assert "integrity evidence" in definition.artifact_expectations


@pytest.mark.parametrize("profile", tuple(BuildProfile))
def test_current_profiles_support_familyos_cli_package(
    profile: BuildProfile,
) -> None:
    definition = validate_profile_target(
        profile,
        BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    assert definition.profile is profile


def test_profile_definition_is_immutable() -> None:
    definition = get_build_profile_definition(BuildProfile.CI)

    with pytest.raises(FrozenInstanceError):
        definition.evidence_required = False  # type: ignore[misc]


@pytest.mark.parametrize(
    (
        "purpose",
        "supported_targets",
        "validation_scope",
        "environment_requirements",
        "artifact_expectations",
        "message",
    ),
    (
        (
            "",
            (BuildTarget.FAMILYOS_CLI_PACKAGE,),
            ("build",),
            ("supported runtime",),
            ("canonical target artifacts",),
            "build profile purpose must not be empty",
        ),
        (
            "purpose",
            (),
            ("build",),
            ("supported runtime",),
            ("canonical target artifacts",),
            "build profile must support at least one target",
        ),
        (
            "purpose",
            (BuildTarget.FAMILYOS_CLI_PACKAGE,),
            (),
            ("supported runtime",),
            ("canonical target artifacts",),
            "build profile must define validation scope",
        ),
        (
            "purpose",
            (BuildTarget.FAMILYOS_CLI_PACKAGE,),
            ("build",),
            (),
            ("canonical target artifacts",),
            "build profile must define environment requirements",
        ),
        (
            "purpose",
            (BuildTarget.FAMILYOS_CLI_PACKAGE,),
            ("build",),
            ("supported runtime",),
            (),
            "build profile must define artifact expectations",
        ),
    ),
)
def test_profile_definition_rejects_incomplete_contract(
    purpose: str,
    supported_targets: tuple[BuildTarget, ...],
    validation_scope: tuple[str, ...],
    environment_requirements: tuple[str, ...],
    artifact_expectations: tuple[str, ...],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        BuildProfileDefinition(
            profile=BuildProfile.DEVELOPMENT,
            purpose=purpose,
            supported_targets=supported_targets,
            validation_scope=validation_scope,
            evidence_required=False,
            environment_requirements=environment_requirements,
            artifact_expectations=artifact_expectations,
        )
