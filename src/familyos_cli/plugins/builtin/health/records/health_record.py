"""Health record model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
    frozen=True,
    slots=True,
)
class HealthRecord:
    """Represent a health record attached to a profile."""

    id: str

    profile_id: str

    record_type: str

    recorded_at: str

    metadata: dict[str, str] = field(
        default_factory=dict,
    )

    def __post_init__(
        self,
    ) -> None:
        """Validate health record."""

        if not self.id.strip():
            raise ValueError(
                "Health record id cannot be empty.",
            )

        if not self.profile_id.strip():
            raise ValueError(
                "Health record profile id cannot be empty.",
            )

        if not self.record_type.strip():
            raise ValueError(
                "Health record type cannot be empty.",
            )

        if not self.recorded_at.strip():
            raise ValueError(
                "Health record date cannot be empty.",
            )
