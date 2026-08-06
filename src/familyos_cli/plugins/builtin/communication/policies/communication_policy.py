"""Communication policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommunicationPolicy:
    """Represents a communication policy."""

    id: str
    name: str
    version: str
    description: str = ""

    def __post_init__(self) -> None:
        """Validate the policy."""

        for value in (
            self.id,
            self.name,
            self.version,
        ):
            if not value.strip():
                raise ValueError(
                    "Communication policy fields must not be empty."
                )
