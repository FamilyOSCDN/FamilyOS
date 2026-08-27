"""In-memory adapter for the canonical Person repository port."""

from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.person import Person, PersonId


class InMemoryPersonRepository(PersonRepository):
    """Store canonical Persons in process memory by PersonId."""

    def __init__(self) -> None:
        self._persons: dict[PersonId, Person] = {}

    def save(self, person: Person) -> None:
        """Persist the canonical Person in memory."""

        self._persons[person.person_id] = person

    def get(self, person_id: PersonId) -> Person | None:
        """Return the Person associated with PersonId, or canonical absence."""

        return self._persons.get(person_id)
