from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.person import Person, PersonId

_PERSON_ID = PersonId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))


def test_person_has_person_id_as_only_intrinsic_state() -> None:
    person = Person(person_id=_PERSON_ID)

    assert person.person_id == _PERSON_ID
    assert [field.name for field in fields(Person)] == ["person_id"]


def test_person_rejects_non_canonical_identity_reference() -> None:
    with pytest.raises(TypeError, match="Person person_id must be a PersonId"):
        Person(person_id=cast(PersonId, "person-001"))


def test_person_is_immutable() -> None:
    person = Person(person_id=_PERSON_ID)

    with pytest.raises(FrozenInstanceError):
        person.person_id = PersonId(  # type: ignore[misc]
            UUID("11234567-89ab-4cde-8f01-23456789abcd")
        )
