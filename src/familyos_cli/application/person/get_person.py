"""Canonical GetPerson application query."""

from __future__ import annotations

from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.person import Person, PersonId


class GetPerson:
    """Retrieve one canonical Person through the repository boundary."""

    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    def execute(self, person_id: PersonId) -> Person | None:
        """Return the canonical Person, or absence when no Person exists."""

        return self._repository.get(person_id)
