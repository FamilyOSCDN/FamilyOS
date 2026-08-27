"""Tests for canonical GetPerson application semantics."""

from uuid import UUID

from familyos_cli.application.person import GetPerson
from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.person import Person, PersonId


class StubPersonRepository(PersonRepository):
    """Minimal repository test double for retrieval semantics."""

    def __init__(self, person: Person | None) -> None:
        self._person = person
        self.requested_person_ids: list[PersonId] = []

    def save(self, person: Person) -> None:
        self._person = person

    def get(self, person_id: PersonId) -> Person | None:
        self.requested_person_ids.append(person_id)

        if self._person is None:
            return None

        if self._person.person_id != person_id:
            return None

        return self._person


def test_get_person_returns_canonical_person_when_present() -> None:
    """Retrieval returns the Person associated with the canonical PersonId."""

    person_id = PersonId(UUID("12345678-1234-4234-8234-123456789abc"))
    person = Person(person_id=person_id)
    repository = StubPersonRepository(person)

    query = GetPerson(repository)

    result = query.execute(person_id)

    assert result == person
    assert repository.requested_person_ids == [person_id]


def test_get_person_returns_none_when_person_is_absent() -> None:
    """Canonical absence remains explicit and distinct from a Person result."""

    person_id = PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    repository = StubPersonRepository(None)

    query = GetPerson(repository)

    result = query.execute(person_id)

    assert result is None
    assert repository.requested_person_ids == [person_id]


def test_get_person_does_not_translate_repository_failure() -> None:
    """Infrastructure failure is not silently converted into Person absence."""

    class FailingRepository(PersonRepository):
        def save(self, person: Person) -> None:
            raise RuntimeError("persistence unavailable")

        def get(self, person_id: PersonId) -> Person | None:
            raise RuntimeError("persistence unavailable")

    query = GetPerson(FailingRepository())
    person_id = PersonId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))

    try:
        query.execute(person_id)
    except RuntimeError as error:
        assert str(error) == "persistence unavailable"
    else:
        raise AssertionError("repository failure must propagate")
