"""Tests for the in-memory Person repository adapter."""

from uuid import UUID

from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.person import Person, PersonId
from familyos_cli.infrastructure.person import InMemoryPersonRepository


def test_repository_implements_canonical_port() -> None:
    repository = InMemoryPersonRepository()

    assert isinstance(repository, PersonRepository)


def test_save_then_get_returns_same_canonical_person() -> None:
    person_id = PersonId(UUID("12345678-1234-4234-8234-123456789abc"))
    person = Person(person_id=person_id)
    repository = InMemoryPersonRepository()

    repository.save(person)

    assert repository.get(person_id) == person


def test_get_returns_none_for_absent_person() -> None:
    repository = InMemoryPersonRepository()
    person_id = PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))

    assert repository.get(person_id) is None


def test_save_replaces_same_person_identity_without_creating_duplicate() -> None:
    person_id = PersonId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))
    first = Person(person_id=person_id)
    second = Person(person_id=person_id)
    repository = InMemoryPersonRepository()

    repository.save(first)
    repository.save(second)

    assert repository.get(person_id) == second
