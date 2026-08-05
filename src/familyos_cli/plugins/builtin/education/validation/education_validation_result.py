"""Education validation result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class EducationValidationResult:
    """Result of education validation."""

    valid: bool

    message: str = ""
