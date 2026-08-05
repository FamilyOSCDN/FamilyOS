"""Finance validation result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class FinanceValidationResult:
    """Result of finance validation."""

    valid: bool

    message: str = ""
