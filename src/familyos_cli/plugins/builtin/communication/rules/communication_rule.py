"""Communication rule."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommunicationRule:
    """Represents a communication rule."""

    id: str
    name: str
    version: str
    severity: str
    description: str = ""

    def __post_init__(self) -> None:
        """Validate the rule."""

        for value in (
            self.id,
            self.name,
            self.version,
            self.severity,
        ):
            if not value.strip():
                raise ValueError(
                    "Communication rule fields must not be empty."
                )
