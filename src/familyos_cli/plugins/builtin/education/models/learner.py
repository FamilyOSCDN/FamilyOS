"""Education learner domain model."""

from __future__ import annotations

from dataclasses import (
    dataclass,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Learner:
    """Represents an education learner."""

    id: str

    name: str

    education_level: str

    def __post_init__(
        self,
    ) -> None:
        """Validate learner state."""

        if not self.id:
            raise ValueError(
                "Learner id cannot be empty.",
            )

        if not self.name:
            raise ValueError(
                "Learner name cannot be empty.",
            )

        if not self.education_level:
            raise ValueError(
                "Learner education level cannot be empty.",
            )
