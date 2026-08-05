"""Education course domain model."""

from __future__ import annotations

from dataclasses import (
    dataclass,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Course:
    """Represents an education course."""

    id: str

    title: str

    description: str

    category: str

    def __post_init__(
        self,
    ) -> None:
        """Validate course state."""

        if not self.id:
            raise ValueError(
                "Course id cannot be empty.",
            )

        if not self.title:
            raise ValueError(
                "Course title cannot be empty.",
            )

        if not self.category:
            raise ValueError(
                "Course category cannot be empty.",
            )
