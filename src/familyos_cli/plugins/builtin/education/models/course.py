"""Education course domain model."""

from __future__ import annotations

from dataclasses import dataclass


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

        if not self.id.strip():
            raise ValueError(
                "Course id cannot be empty.",
            )

        if not self.title.strip():
            raise ValueError(
                "Course title cannot be empty.",
            )

        if not self.category.strip():
            raise ValueError(
                "Course category cannot be empty.",
            )
