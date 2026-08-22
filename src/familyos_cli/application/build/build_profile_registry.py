"""Canonical registry of supported Build Framework profiles."""

from __future__ import annotations

from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_profile_definition import (
    BuildProfileDefinition,
)

_FAMILYOS_CLI_TARGETS = (
    BuildTarget.FAMILYOS_CLI_PACKAGE,
)

_DEVELOPMENT = BuildProfileDefinition(
    profile=BuildProfile.DEVELOPMENT,
    purpose="Support everyday local engineering with rapid feedback.",
    supported_targets=_FAMILYOS_CLI_TARGETS,
    validation_scope=(
        "configuration",
        "essential dependencies",
        "basic build execution",
        "artifact presence",
        "basic artifact validation",
    ),
    evidence_required=False,
    environment_requirements=(
        "supported runtime",
        "declared dependencies",
        "required validation tools",
        "canonical build tools",
        "practical local isolation",
    ),
    artifact_expectations=(
        "canonical target artifacts",
    ),
)

_VALIDATION = BuildProfileDefinition(
    profile=BuildProfile.VALIDATION,
    purpose=(
        "Verify that the current engineering state satisfies required "
        "validation under a controlled environment."
    ),
    supported_targets=_FAMILYOS_CLI_TARGETS,
    validation_scope=(
        "ruff",
        "mypy",
        "pytest",
        "packaging checks",
        "structural checks",
    ),
    evidence_required=False,
    environment_requirements=(
        "controlled validation environment",
        "supported runtime",
        "declared dependencies",
        "canonical validation tools",
    ),
    artifact_expectations=(
        "canonical target artifacts",
        "structurally valid artifacts",
    ),
)

_CI = BuildProfileDefinition(
    profile=BuildProfile.CI,
    purpose=(
        "Execute canonical validation and build behavior in an independently "
        "provisioned automation environment."
    ),
    supported_targets=_FAMILYOS_CLI_TARGETS,
    validation_scope=(
        "canonical environment",
        "static validation",
        "tests",
        "build",
        "artifact validation",
        "evidence generation",
    ),
    evidence_required=True,
    environment_requirements=(
        "fresh environment",
        "explicit dependency installation",
        "canonical build commands",
        "isolated secrets",
        "standard evidence",
    ),
    artifact_expectations=(
        "canonical target artifacts",
        "validated artifacts",
        "build evidence",
    ),
)

_RELEASE_CANDIDATE = BuildProfileDefinition(
    profile=BuildProfile.RELEASE_CANDIDATE,
    purpose=(
        "Produce release-candidate artifacts under the strongest current "
        "Build Framework controls."
    ),
    supported_targets=_FAMILYOS_CLI_TARGETS,
    validation_scope=(
        "source state validation",
        "configuration validation",
        "dependency validation",
        "toolchain validation",
        "environment validation",
        "build execution",
        "artifact validation",
        "integrity validation",
        "evidence validation",
        "release readiness",
    ),
    evidence_required=True,
    environment_requirements=(
        "canonical runtime version",
        "controlled dependency state",
        "validated canonical toolchain",
        "explicit source revision",
        "clean workspace",
        "stronger evidence",
    ),
    artifact_expectations=(
        "canonical target artifacts",
        "validated artifacts",
        "integrity evidence",
        "release-candidate evidence",
    ),
)

_PROFILES = {
    definition.profile: definition
    for definition in (
        _DEVELOPMENT,
        _VALIDATION,
        _CI,
        _RELEASE_CANDIDATE,
    )
}


def get_build_profile_definition(
    profile: BuildProfile,
) -> BuildProfileDefinition:
    """Return the canonical definition for one supported build profile."""

    try:
        return _PROFILES[profile]
    except KeyError as error:
        raise ValueError(
            f"unsupported build profile: {profile.value}"
        ) from error


def validate_profile_target(
    profile: BuildProfile,
    target: BuildTarget,
) -> BuildProfileDefinition:
    """Resolve a profile and reject unsupported target combinations."""

    definition = get_build_profile_definition(profile)

    if target not in definition.supported_targets:
        raise ValueError(
            "unsupported build profile/target combination: "
            f"{profile.value}/{target.value}"
        )

    return definition
