"""Immutable result model for canonical CI validation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final

CI_VALIDATION_SCHEMA_VERSION: Final = "1.0.0"
CI_VALIDATION_PROFILE: Final = "ci"
MANDATORY_CI_GATE_IDS: Final = (
    "dependency-freshness",
    "dependency-consistency",
    "ruff",
    "mypy",
    "pytest",
    "builtin-plugin-compliance",
)


class ValidationStatus(StrEnum):
    """Canonical validation outcome ordered by severity."""

    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class PluginRuleSummary:
    """Deterministic semantic summary of one compliance rule."""

    rule_id: str
    outcome: str
    severity: str


@dataclass(frozen=True, slots=True)
class PluginValidationSummary:
    """Deterministic semantic summary of one builtin plugin evaluation."""

    plugin_id: str
    plugin_version: str
    status: str
    rule_outcomes: tuple[PluginRuleSummary, ...]
    diagnostic: str | None = None


@dataclass(frozen=True, slots=True)
class GateResult:
    """Result of one mandatory canonical validation gate."""

    gate_id: str
    status: ValidationStatus
    exit_code: int | None = None
    diagnostic: str | None = None
    profile_id: str | None = None
    plugins: tuple[PluginValidationSummary, ...] = ()


@dataclass(frozen=True, slots=True)
class CiValidationResult:
    """Aggregate result preserving every gate in canonical order."""

    gates: tuple[GateResult, ...]
    schema_version: str = CI_VALIDATION_SCHEMA_VERSION
    profile: str = CI_VALIDATION_PROFILE

    @property
    def status(self) -> ValidationStatus:
        """Return ERROR before FAILED, and PASSED only when all gates pass."""

        statuses = {gate.status for gate in self.gates}
        if ValidationStatus.ERROR in statuses:
            return ValidationStatus.ERROR
        if ValidationStatus.FAILED in statuses:
            return ValidationStatus.FAILED
        return ValidationStatus.PASSED

    @property
    def successful(self) -> bool:
        """Return whether every mandatory gate passed."""

        return self.status is ValidationStatus.PASSED
