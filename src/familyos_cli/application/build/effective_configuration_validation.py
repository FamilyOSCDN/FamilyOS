"""Canonical effective build-configuration validation result models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EffectiveConfigurationValidationStatus(StrEnum):
    """Outcome of final effective-configuration validation."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class EffectiveConfigurationValidationFinding:
    """One deterministic effective-configuration validation failure."""

    component: str
    diagnostic: str

    def __post_init__(self) -> None:
        """Reject incomplete effective-configuration findings."""

        if not self.component:
            raise ValueError(
                "effective configuration validation component must not be empty",
            )

        if not self.diagnostic:
            raise ValueError(
                "effective configuration validation diagnostic must not be empty",
            )


@dataclass(frozen=True, slots=True)
class EffectiveConfigurationValidationResult:
    """Canonical decision for one resolved effective build configuration."""

    status: EffectiveConfigurationValidationStatus
    findings: tuple[EffectiveConfigurationValidationFinding, ...] = ()

    def __post_init__(self) -> None:
        """Require findings exactly when validation fails."""

        if (
            self.status is EffectiveConfigurationValidationStatus.SUCCEEDED
            and self.findings
        ):
            raise ValueError(
                "successful effective configuration validation must not "
                "contain findings",
            )

        if (
            self.status is EffectiveConfigurationValidationStatus.FAILED
            and not self.findings
        ):
            raise ValueError(
                "failed effective configuration validation requires findings",
            )

    @property
    def successful(self) -> bool:
        """Return whether the resolved effective configuration is coherent."""

        return self.status is EffectiveConfigurationValidationStatus.SUCCEEDED

    @property
    def diagnostic(self) -> str | None:
        """Return deterministic combined failure diagnostics."""

        if not self.findings:
            return None

        return "; ".join(
            finding.diagnostic
            for finding in self.findings
        )
