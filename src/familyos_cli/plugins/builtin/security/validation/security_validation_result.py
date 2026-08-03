"""Security validation result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class SecurityValidationResult:
    """Represent a security validation result."""

    valid: bool

    message: str = ""
