"""Canonical build input validation models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BuildInputValidationCheck:
    """One build input validation result."""

    input_name: str
    successful: bool
    diagnostic: str | None = None


@dataclass(frozen=True, slots=True)
class BuildInputValidationResult:
    """Aggregate build input validation result."""

    checks: tuple[BuildInputValidationCheck, ...]

    @property
    def successful(self) -> bool:
        """Return whether all required inputs are valid."""

        return all(
            check.successful
            for check in self.checks
        )

    @property
    def diagnostic(self) -> str | None:
        """Return the first failed input diagnostic."""

        for check in self.checks:
            if not check.successful:
                return check.diagnostic

        return None
