"""Canonical environment-validation result for build execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EnvironmentValidationStatus(StrEnum):
    """Outcome of canonical build-environment validation."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class EnvironmentValidationFinding:
    """One deterministic environment-validation failure."""

    component: str
    diagnostic: str

    def __post_init__(self) -> None:
        """Reject incomplete environment-validation findings."""

        if not self.component:
            raise ValueError(
                "environment validation component must not be empty",
            )

        if not self.diagnostic:
            raise ValueError(
                "environment validation diagnostic must not be empty",
            )


@dataclass(frozen=True, slots=True)
class EnvironmentValidationResult:
    """Result of canonical build-environment validation."""

    status: EnvironmentValidationStatus
    findings: tuple[EnvironmentValidationFinding, ...] = ()

    def __post_init__(self) -> None:
        """Require findings exactly when validation fails."""

        if (
            self.status is EnvironmentValidationStatus.SUCCEEDED
            and self.findings
        ):
            raise ValueError(
                "successful environment validation must not contain findings",
            )

        if (
            self.status is EnvironmentValidationStatus.FAILED
            and not self.findings
        ):
            raise ValueError(
                "failed environment validation requires findings",
            )

    @property
    def successful(self) -> bool:
        """Return whether canonical environment validation succeeded."""

        return self.status is EnvironmentValidationStatus.SUCCEEDED

    @property
    def diagnostic(self) -> str | None:
        """Return deterministic combined failure diagnostics."""

        if not self.findings:
            return None

        return "; ".join(
            finding.diagnostic
            for finding in self.findings
        )
