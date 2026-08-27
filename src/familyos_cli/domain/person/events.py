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
        """Require canonical identity and an unambiguous occurrence instant."""
        if not isinstance(self.person_id, PersonId):
            raise TypeError("PersonCreated person_id must be a PersonId")

        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("PersonCreated occurrence time must be timezone-aware")
