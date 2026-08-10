"""Document validation result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentValidationResult:
    """Result of document validation."""

    valid: bool

    message: str = ""