"""Tests for the in-memory Person repository adapter."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import UUID

import pytest

from familyos_cli.application.ports.person import (
    PersonConflictError,
    PersonRepository,
)
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


def test_save_rejects_established_identity_without_replacing_person() -> None:
    person_id = PersonId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))
    first = Person(person_id=person_id)
    second = Person(person_id=person_id)
    repository = InMemoryPersonRepository()

    repository.save(first)

    with pytest.raises(
        PersonConflictError,
        match=f"Person '{person_id}' already exists",
    ):
        repository.save(second)

    assert repository.get(person_id) is first


def test_concurrent_save_establishes_identity_exactly_once() -> None:
    person_id = PersonId(UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))
    persons = tuple(Person(person_id=person_id) for _ in range(8))
    barrier = Barrier(len(persons))
    repository = InMemoryPersonRepository()

    def attempt_save(person: Person) -> bool:
        barrier.wait()

        try:
            repository.save(person)
        except PersonConflictError:
            return False

        return True

    with ThreadPoolExecutor(max_workers=len(persons)) as executor:
        outcomes = tuple(executor.map(attempt_save, persons))

    assert outcomes.count(True) == 1
    assert outcomes.count(False) == len(persons) - 1
    assert repository.get(person_id) is persons[outcomes.index(True)]
