from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import FamilyId

_UUID4 = UUID("01234567-89ab-4cde-8f01-23456789abcd")


def test_family_id_wraps_uuid4() -> None:
    family_id = FamilyId(_UUID4)

    assert family_id.value == _UUID4


def test_family_id_rejects_non_uuid_backing_value() -> None:
    with pytest.raises(TypeError, match="FamilyId value must be a UUID"):
        FamilyId(cast(UUID, object()))


def test_family_id_does_not_reinterpret_legacy_string() -> None:
    with pytest.raises(TypeError, match="FamilyId value must be a UUID"):
        FamilyId(cast(UUID, "family-001"))


def test_family_id_rejects_uuid_formatted_string() -> None:
    uuid_text = "12345678-1234-4234-8234-123456789abc"

    with pytest.raises(TypeError, match="FamilyId value must be a UUID"):
        FamilyId(cast(UUID, uuid_text))


def test_family_id_rejects_non_uuid4_identity() -> None:
    uuid1 = UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

    with pytest.raises(ValueError, match="FamilyId value must be a UUID version 4"):
        FamilyId(uuid1)


def test_family_id_is_value_comparable() -> None:
    assert FamilyId(_UUID4) == FamilyId(_UUID4)


def test_family_id_is_immutable() -> None:
    family_id = FamilyId(_UUID4)

    with pytest.raises(FrozenInstanceError):
        family_id.value = UUID(  # type: ignore[misc]
            "11234567-89ab-4cde-8f01-23456789abcd"
        )


def test_family_id_generate_returns_uuid4_backed_identity() -> None:
    family_id = FamilyId.generate()

    assert isinstance(family_id.value, UUID)
    assert family_id.value.version == 4


def test_family_id_string_is_canonical_uuid() -> None:
    assert str(FamilyId(_UUID4)) == str(_UUID4)
