"""Canonical build-toolchain validation result models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ToolchainValidationStatus(StrEnum):
    """Outcome of canonical build-toolchain validation."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ToolchainValidationFinding:
    """One deterministic toolchain compatibility finding."""

    component: str
    diagnostic: str

    def __post_init__(self) -> None:
        """Reject incomplete validation findings."""

        if not self.component:
            raise ValueError("toolchain validation component must not be empty")

        if not self.diagnostic:
            raise ValueError("toolchain validation diagnostic must not be empty")


@dataclass(frozen=True, slots=True)
class ToolchainValidationResult:
    """Canonical decision for one observed build toolchain."""

    status: ToolchainValidationStatus
    findings: tuple[ToolchainValidationFinding, ...] = ()

    def __post_init__(self) -> None:
        """Require status and findings to agree."""

        if (
            self.status is ToolchainValidationStatus.SUCCEEDED
            and self.findings
        ):
            raise ValueError(
                "successful toolchain validation must not contain findings",
            )

        if (
            self.status is ToolchainValidationStatus.FAILED
            and not self.findings
        ):
            raise ValueError(
                "failed toolchain validation must contain findings",
            )

    @property
    def successful(self) -> bool:
        """Return whether the observed toolchain is compatible."""

        return self.status is ToolchainValidationStatus.SUCCEEDED

    @property
    def diagnostic(self) -> str | None:
        """Return a deterministic aggregate diagnostic when validation fails."""

        if not self.findings:
            return None

        return "; ".join(finding.diagnostic for finding in self.findings)
