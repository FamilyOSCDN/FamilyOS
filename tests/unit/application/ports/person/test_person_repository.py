"""Tests for the canonical PersonRepository port."""

from __future__ import annotations

import inspect

import pytest

from familyos_cli.application.ports.person import (
    PersonConflictError,
    PersonRepository,
)
from familyos_cli.domain.person import Person, PersonId


def test_person_repository_is_abstract() -> None:
    """The canonical repository contract must remain abstract."""

    assert inspect.isabstract(PersonRepository)


def test_person_repository_cannot_be_instantiated() -> None:
    """The persistence port must not provide a concrete persistence mechanism."""

    with pytest.raises(TypeError):
        PersonRepository()  # type: ignore[abstract]


def test_concrete_repository_can_implement_canonical_contract() -> None:
    """A concrete adapter can implement only save and get."""

    class Repository(PersonRepository):
        def __init__(self) -> None:
            self._persons: dict[PersonId, Person] = {}

        def save(self, person: Person) -> None:
            if person.person_id in self._persons:
                raise PersonConflictError

            self._persons[person.person_id] = person

        def get(self, person_id: PersonId) -> Person | None:
            return self._persons.get(person_id)

    repository = Repository()
    person = Person(person_id=PersonId.generate())

    assert repository.get(person.person_id) is None

    repository.save(person)

    assert repository.get(person.person_id) == person


def test_person_repository_exposes_only_canonical_repository_operations() -> None:
    """Future Person capabilities must not leak into the repository port."""

    public_operations = {
        name
        for name, member in inspect.getmembers(PersonRepository, inspect.isfunction)
        if not name.startswith("_")
    }

    assert public_operations == {"get", "save"}
