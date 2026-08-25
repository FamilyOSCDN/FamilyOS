"""Canonical Build Validation orchestration result models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from familyos_cli.application.build.build_id import BuildId


class BuildValidationProfile(StrEnum):
    """Canonical Build Validation profiles."""

    DEVELOPMENT = "development"
    VALIDATION = "validation"
    CI = "ci"
    RELEASE_CANDIDATE = "release-candidate"


class BuildValidationRequirement(StrEnum):
    """Decision importance assigned to one validation check."""

    REQUIRED = "required"
    OPTIONAL = "optional"
    INFORMATIONAL = "informational"


class BuildValidationStatus(StrEnum):
    """Outcome of one check or an aggregate Build Validation decision."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class BuildValidationDomain(StrEnum):
    """Canonical validation domains owned or coordinated by Build Validation."""

    INPUT = "input"
    SOURCE = "source"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    TOOLCHAIN = "toolchain"
    ENVIRONMENT = "environment"
    TESTING = "testing"
    COMPLIANCE = "compliance"
    EXECUTION = "execution"
    ARTIFACT = "artifact"
    METADATA = "metadata"
    INTEGRITY = "integrity"
    FUNCTIONAL_ARTIFACT = "functional-artifact"
    EVIDENCE = "evidence"


@dataclass(frozen=True, slots=True)
class BuildValidationCheckResult:
    """Result of one explicitly classified Build Validation check."""

    check_id: str
    domain: BuildValidationDomain
    requirement: BuildValidationRequirement
    status: BuildValidationStatus
    diagnostic: str | None = None


@dataclass(frozen=True, slots=True)
class BuildValidationResult:
    """Aggregate decision for one Build Validation profile and Build ID."""

    build_id: BuildId
    profile: BuildValidationProfile
    checks: tuple[BuildValidationCheckResult, ...]
    status: BuildValidationStatus

    @property
    def successful(self) -> bool:
        """Return whether mandatory Build Validation requirements passed."""

        return self.status is BuildValidationStatus.PASSED

    @property
    def failures(self) -> tuple[BuildValidationCheckResult, ...]:
        """Return failed required checks."""

        return tuple(
            check
            for check in self.checks
            if check.requirement is BuildValidationRequirement.REQUIRED
            and check.status is BuildValidationStatus.FAILED
        )

    @property
    def warnings(self) -> tuple[BuildValidationCheckResult, ...]:
        """Return failed optional checks."""

        return tuple(
            check
            for check in self.checks
            if check.requirement is BuildValidationRequirement.OPTIONAL
            and check.status is BuildValidationStatus.FAILED
        )
