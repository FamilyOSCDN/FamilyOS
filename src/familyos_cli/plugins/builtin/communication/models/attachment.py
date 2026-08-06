"""Communication attachment model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Attachment:
    """Represents a communication attachment."""

    identifier: str
    filename: str
    media_type: str
    size: int

    def __post_init__(self) -> None:
        """Validate attachment."""

        for field in (
            self.identifier,
            self.filename,
            self.media_type,
        ):
            if not field.strip():
                raise ValueError(
                    "Attachment fields must not be empty."
                )

        if self.size < 0:
            raise ValueError(
                "Attachment size must be non-negative."
            )
