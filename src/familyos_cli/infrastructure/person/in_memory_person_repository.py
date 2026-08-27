"""In-memory adapter for the canonical Person repository port."""

from threading import Lock

from familyos_cli.application.ports.person import (
    PersonConflictError,
    PersonRepository,
)
from familyos_cli.domain.person import Person, PersonId


class InMemoryPersonRepository(PersonRepository):
    """Store canonical Persons in process memory by PersonId."""

    def __init__(self) -> None:
        self._persons: dict[PersonId, Person] = {}
        self._lock = Lock()

    def save(self, person: Person) -> None:
        """Atomically establish the Person without replacing its identity."""

        with self._lock:
            if person.person_id in self._persons:
                raise PersonConflictError(f"Person '{person.person_id}' already exists")

            self._persons[person.person_id] = person

    def get(self, person_id: PersonId) -> Person | None:
        """Return the Person associated with PersonId, or canonical absence."""

        with self._lock:
            return self._persons.get(person_id)
