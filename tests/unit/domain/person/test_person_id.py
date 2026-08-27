from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.person import PersonId

_UUID = UUID("01234567-89ab-4cde-8f01-23456789abcd")


def test_person_id_wraps_uuid() -> None:
    person_id = PersonId(_UUID)

    assert person_id.value == _UUID


def test_person_id_rejects_non_uuid_backing_value() -> None:
    with pytest.raises(TypeError, match="PersonId value must be a UUID"):
        PersonId(cast(UUID, object()))


def test_person_id_does_not_reinterpret_legacy_string() -> None:
    with pytest.raises(TypeError, match="PersonId value must be a UUID"):
        PersonId(cast(UUID, "person-001"))


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


def test_person_id_rejects_uuid_formatted_string() -> None:
    """A UUID-formatted string is not itself a canonical UUID value."""

    uuid_text = "12345678-1234-4234-8234-123456789abc"

    with pytest.raises(TypeError, match="PersonId value must be a UUID"):
        PersonId(cast(UUID, uuid_text))
