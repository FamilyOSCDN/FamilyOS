from dataclasses import FrozenInstanceError, fields
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import Family, FamilyId

_FAMILY_ID = FamilyId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))


def test_family_has_family_id_as_only_intrinsic_state() -> None:
    family = Family(family_id=_FAMILY_ID)

    assert family.family_id == _FAMILY_ID
    assert [field.name for field in fields(Family)] == ["family_id"]


def test_family_rejects_non_canonical_identity_reference() -> None:
    with pytest.raises(TypeError, match="Family family_id must be a FamilyId"):
        Family(family_id=cast(FamilyId, "family-001"))


def test_family_is_immutable() -> None:
    family = Family(family_id=_FAMILY_ID)

    with pytest.raises(FrozenInstanceError):
        family.family_id = FamilyId(  # type: ignore[misc]
            UUID("11234567-89ab-4cde-8f01-23456789abcd")
        )
