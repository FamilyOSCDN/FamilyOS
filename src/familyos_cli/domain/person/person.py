"""Canonical Person aggregate root."""

from dataclasses import dataclass

from familyos_cli.domain.person.person_id import PersonId


@dataclass(frozen=True, slots=True)
class Person:
    """Minimal canonical Person with identity as its only intrinsic state."""

    person_id: PersonId

    def __post_init__(self) -> None:
        """Require the canonical Person identity value object."""
        if not isinstance(self.person_id, PersonId):
            raise TypeError("Person person_id must be a PersonId")
