"""Persistence port for the canonical Person domain."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.domain.person import Person, PersonId


class PersonRepository(ABC):
    """Persist and retrieve canonical Person aggregates."""

    @abstractmethod
    def save(self, person: Person) -> None:
        """Persist one canonical Person."""

        raise NotImplementedError

    @abstractmethod
    def get(self, person_id: PersonId) -> Person | None:
        """Return one Person, or absence when no Person exists for the identifier."""

        raise NotImplementedError
