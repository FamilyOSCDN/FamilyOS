"""Canonical Person domain core."""

from familyos_cli.domain.person.events import PersonCreated
from familyos_cli.domain.person.person import Person
from familyos_cli.domain.person.person_id import PersonId

__all__ = [
    "Person",
    "PersonCreated",
    "PersonId",
]
