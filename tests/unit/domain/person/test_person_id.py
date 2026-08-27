from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from familyos_cli.domain.person import PersonId

_UUID = UUID("01234567-89ab-4cde-8f01-23456789abcd")


def test_person_id_wraps_uuid() -> None:
    person_id = PersonId(_UUID)

    assert person_id.value == _UUID


def test_person_id_is_value_comparable() -> None:
    assert PersonId(_UUID) == PersonId(_UUID)


def test_person_id_is_immutable() -> None:
    person_id = PersonId(_UUID)

    with pytest.raises(FrozenInstanceError):
        person_id.value = UUID(  # type: ignore[misc]
            "11234567-89ab-4cde-8f01-23456789abcd"
        )


def test_person_id_generate_returns_uuid4_backed_identity() -> None:
    person_id = PersonId.generate()

    assert isinstance(person_id.value, UUID)
    assert person_id.value.version == 4


def test_person_id_string_is_canonical_uuid() -> None:
    assert str(PersonId(_UUID)) == str(_UUID)
