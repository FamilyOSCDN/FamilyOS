"""Canonical execution-stage observations for package builds."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class BuildExecutionStage(StrEnum):
    """Canonical stages of the current package-build orchestration."""

    VALIDATE_INPUTS = "validate-inputs"
    VALIDATE_REPOSITORY_LAYOUT = "validate-repository-layout"
    VALIDATE_TOOLCHAIN = "validate-toolchain"
    VALIDATE_ENVIRONMENT = "validate-environment"
    INITIALIZE_WORKSPACE = "initialize-workspace"
    RESOLVE_BUILD_CONTEXT = "resolve-build-context"
    VALIDATE_EFFECTIVE_CONFIGURATION = "validate-effective-configuration"
    STAGE_BUILD_INPUTS = "stage-build-inputs"
    PACKAGE = "package"
    DISCOVER_ARTIFACTS = "discover-artifacts"
    VALIDATE_ARTIFACTS = "validate-artifacts"
    ESTABLISH_ARTIFACT_IDENTITY = "establish-artifact-identity"
    ESTABLISH_ARTIFACT_INTEGRITY = "establish-artifact-integrity"
    BUILD_ARTIFACT_MANIFEST = "build-artifact-manifest"
    FUNCTIONALLY_VALIDATE_WHEEL = "functionally-validate-wheel"
    FINALIZE_EXECUTION = "finalize-execution"


class BuildExecutionStageStatus(StrEnum):
    """Terminal outcome of an observed canonical execution stage."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class BuildExecutionObservation:
    """Immutable observation of one completed canonical execution stage."""

    stage: BuildExecutionStage
    status: BuildExecutionStageStatus
    duration_seconds: float
    diagnostic: str | None = None
