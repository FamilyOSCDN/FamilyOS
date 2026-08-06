"""Communication participant model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Participant:
    """Represents a communication participant."""

    identifier: str
    display_name: str
    address: str

    def __post_init__(self) -> None:
        """Validate participant."""

        for field in (
            self.identifier,
            self.display_name,
            self.address,
        ):
            if not field.strip():
                raise ValueError(
                    "Participant fields must not be empty."
                )
