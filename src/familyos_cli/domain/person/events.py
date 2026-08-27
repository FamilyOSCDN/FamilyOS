"""Canonical Person domain events."""

from dataclasses import dataclass
from datetime import datetime

from familyos_cli.domain.person.person_id import PersonId


@dataclass(frozen=True, slots=True)
class PersonCreated:
    """Immutable fact that one canonical Person was successfully created."""

    person_id: PersonId
    occurred_at: datetime

    def __post_init__(self) -> None:
        """Require an unambiguous timezone-aware occurrence instant."""
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("PersonCreated occurrence time must be timezone-aware")
