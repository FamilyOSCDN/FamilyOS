"""Health profile model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
    frozen=True,
    slots=True,
)
class HealthProfile:
    """Represent a family member health profile."""

    id: str

    person_id: str

    status: str = "active"

    metadata: dict[str, str] = field(
        default_factory=dict,
    )

    def __post_init__(
        self,
    ) -> None:
        """Validate health profile."""

        if not self.id:
            raise ValueError(
                "Health profile id cannot be empty.",
            )

        if not self.person_id:
            raise ValueError(
                "Health profile person id cannot be empty.",
            )
