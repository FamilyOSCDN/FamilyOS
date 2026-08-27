"""Canonical CreatePerson application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.person import Person, PersonCreated, PersonId


@dataclass(frozen=True, slots=True)
class CreatePersonResult:
    """Successful canonical Person creation result."""

    person: Person
    event: PersonCreated


class CreatePerson:
    """Create and persist exactly one canonical Person."""

    def __init__(
        self,
        repository: PersonRepository,
        *,
        person_id_factory: Callable[[], PersonId] = PersonId.generate,
        clock: Callable[[], datetime],
    ) -> None:
        self._repository = repository
        self._person_id_factory = person_id_factory
        self._clock = clock

    def execute(self) -> CreatePersonResult:
        """Create, persist, and report one canonical Person."""

        person = Person(person_id=self._person_id_factory())
        self._repository.save(person)

        event = PersonCreated(
            person_id=person.person_id,
            occurred_at=self._clock(),
        )
        return CreatePersonResult(person=person, event=event)
