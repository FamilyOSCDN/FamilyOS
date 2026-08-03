"""Health validation result."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
    frozen=True,
    slots=True,
)
class HealthValidationResult:
    """Represent health validation outcome."""

    valid: bool

    errors: tuple[str, ...] = field(
        default_factory=tuple,
    )

    @classmethod
    def success(
        cls,
    ) -> HealthValidationResult:
        """Create successful validation result."""

        return cls(
            valid=True,
        )

    @classmethod
    def failure(
        cls,
        errors: tuple[str, ...],
    ) -> HealthValidationResult:
        """Create failed validation result."""

        return cls(
            valid=False,
            errors=errors,
        )
