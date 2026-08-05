"""Educational record domain model."""

from __future__ import annotations

from dataclasses import (
    dataclass,
)


@dataclass(
    frozen=True,
    slots=True,
)
class EducationalRecord:
    """Represents an educational record."""

    id: str

    learner_id: str

    course_id: str

    result: str

    def __post_init__(
        self,
    ) -> None:
        """Validate educational record state."""

        if not self.id:
            raise ValueError(
                "EducationalRecord id cannot be empty.",
            )

        if not self.learner_id:
            raise ValueError(
                "EducationalRecord learner id cannot be empty.",
            )

        if not self.course_id:
            raise ValueError(
                "EducationalRecord course id cannot be empty.",
            )

        if not self.result:
            raise ValueError(
                "EducationalRecord result cannot be empty.",
            )
