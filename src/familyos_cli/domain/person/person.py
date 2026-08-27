"""Canonical Person aggregate root."""

from dataclasses import dataclass

from familyos_cli.domain.person.person_id import PersonId


@dataclass(frozen=True, slots=True)
class Person:
    """Minimal canonical Person with identity as its only intrinsic state."""

    person_id: PersonId
