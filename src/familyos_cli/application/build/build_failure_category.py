"""Canonical Build failure categories."""

from enum import StrEnum

from familyos_cli.application.build.build_execution_observation import (
    BuildExecutionStage,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationDomain,
)


class BuildFailureCategory(StrEnum):
    """High-level canonical classification for a failed Build result."""

    INPUT = "input"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    TOOLCHAIN = "toolchain"
    ENVIRONMENT = "environment"
    EXECUTION = "execution"
    ARTIFACT = "artifact"
    VALIDATION = "validation"
    INTEGRITY = "integrity"

_VALIDATION_DOMAIN_FAILURE_CATEGORIES: dict[
    BuildValidationDomain,
    BuildFailureCategory,
] = {
    BuildValidationDomain.INPUT: BuildFailureCategory.INPUT,
    BuildValidationDomain.SOURCE: BuildFailureCategory.INPUT,
    BuildValidationDomain.CONFIGURATION: BuildFailureCategory.CONFIGURATION,
    BuildValidationDomain.DEPENDENCY: BuildFailureCategory.DEPENDENCY,
    BuildValidationDomain.TOOLCHAIN: BuildFailureCategory.TOOLCHAIN,
    BuildValidationDomain.ENVIRONMENT: BuildFailureCategory.ENVIRONMENT,
    BuildValidationDomain.TESTING: BuildFailureCategory.VALIDATION,
    BuildValidationDomain.COMPLIANCE: BuildFailureCategory.VALIDATION,
    BuildValidationDomain.EXECUTION: BuildFailureCategory.EXECUTION,
    BuildValidationDomain.ARTIFACT: BuildFailureCategory.ARTIFACT,
    BuildValidationDomain.METADATA: BuildFailureCategory.ARTIFACT,
    BuildValidationDomain.INTEGRITY: BuildFailureCategory.INTEGRITY,
    BuildValidationDomain.FUNCTIONAL_ARTIFACT: BuildFailureCategory.ARTIFACT,
    BuildValidationDomain.EVIDENCE: BuildFailureCategory.VALIDATION,
}


def failure_category_for_validation_domain(
    domain: BuildValidationDomain,
) -> BuildFailureCategory:
    """Project one canonical validation domain to its failure category."""

    return _VALIDATION_DOMAIN_FAILURE_CATEGORIES[domain]


_EXECUTION_STAGE_FAILURE_CATEGORIES: dict[
    BuildExecutionStage,
    BuildFailureCategory,
] = {
    BuildExecutionStage.VALIDATE_INPUTS: BuildFailureCategory.INPUT,
    BuildExecutionStage.VALIDATE_REPOSITORY_LAYOUT: BuildFailureCategory.INPUT,
    BuildExecutionStage.VALIDATE_TOOLCHAIN: BuildFailureCategory.TOOLCHAIN,
    BuildExecutionStage.VALIDATE_ENVIRONMENT: BuildFailureCategory.ENVIRONMENT,
    BuildExecutionStage.INITIALIZE_WORKSPACE: BuildFailureCategory.ENVIRONMENT,
    BuildExecutionStage.RESOLVE_BUILD_CONTEXT: BuildFailureCategory.CONFIGURATION,
    BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION: (
        BuildFailureCategory.CONFIGURATION
    ),
    BuildExecutionStage.STAGE_BUILD_INPUTS: BuildFailureCategory.INPUT,
    BuildExecutionStage.PACKAGE: BuildFailureCategory.EXECUTION,
    BuildExecutionStage.DISCOVER_ARTIFACTS: BuildFailureCategory.ARTIFACT,
    BuildExecutionStage.VALIDATE_ARTIFACTS: BuildFailureCategory.ARTIFACT,
    BuildExecutionStage.ESTABLISH_ARTIFACT_IDENTITY: (
        BuildFailureCategory.ARTIFACT
    ),
    BuildExecutionStage.ESTABLISH_ARTIFACT_INTEGRITY: (
        BuildFailureCategory.INTEGRITY
    ),
    BuildExecutionStage.BUILD_ARTIFACT_MANIFEST: BuildFailureCategory.ARTIFACT,
    BuildExecutionStage.FUNCTIONALLY_VALIDATE_WHEEL: (
        BuildFailureCategory.ARTIFACT
    ),
    BuildExecutionStage.FINALIZE_EXECUTION: BuildFailureCategory.EXECUTION,
}


def failure_category_for_execution_stage(
    stage: BuildExecutionStage,
) -> BuildFailureCategory:
    """Project one canonical execution stage to its failure category."""

    return _EXECUTION_STAGE_FAILURE_CATEGORIES[stage]


_CORRECTIVE_INFORMATION_BY_FAILURE_CATEGORY: dict[
    BuildFailureCategory,
    str,
] = {
    BuildFailureCategory.INPUT:
        "Correct the invalid build input and retry.",
    BuildFailureCategory.CONFIGURATION:
        "Correct the effective build configuration and retry.",
    BuildFailureCategory.DEPENDENCY:
        "Restore the required dependency state and retry.",
    BuildFailureCategory.TOOLCHAIN:
        "Restore the required build toolchain and retry.",
    BuildFailureCategory.ENVIRONMENT:
        "Correct the build environment and retry.",
    BuildFailureCategory.EXECUTION:
        "Correct the failed build execution condition and retry.",
    BuildFailureCategory.ARTIFACT:
        "Correct the generated artifact and retry the build.",
    BuildFailureCategory.VALIDATION:
        "Correct the failed validation requirement and retry.",
    BuildFailureCategory.INTEGRITY:
        "Restore artifact integrity before continuing.",
}


def corrective_information_for_failure_category(
    category: BuildFailureCategory,
) -> str:
    """Return stable corrective direction for one failure category."""

    return _CORRECTIVE_INFORMATION_BY_FAILURE_CATEGORY[category]
