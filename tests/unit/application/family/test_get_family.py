"""Tests for canonical GetFamily application semantics."""

from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import GetFamily
from familyos_cli.application.ports.family import FamilyRepository
from familyos_cli.domain.family import Family, FamilyId


class StubFamilyRepository(FamilyRepository):
    """Minimal repository test double for retrieval semantics."""

    def __init__(self, family: Family | None) -> None:
        self._family = family
        self.requested_family_ids: list[FamilyId] = []

    def save(self, family: Family) -> None:
        self._family = family

    def get(self, family_id: FamilyId) -> Family | None:
        self.requested_family_ids.append(family_id)

        if self._family is None:
            return None

        if self._family.family_id != family_id:
            return None

        return self._family


def test_get_family_returns_canonical_family_when_present() -> None:
    family_id = FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))
    family = Family(family_id=family_id)
    repository = StubFamilyRepository(family)

    result = GetFamily(repository).execute(family_id)

    assert result == family
    assert repository.requested_family_ids == [family_id]


def test_get_family_returns_none_when_family_is_absent() -> None:
    family_id = FamilyId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    repository = StubFamilyRepository(None)

    result = GetFamily(repository).execute(family_id)

    assert result is None
    assert repository.requested_family_ids == [family_id]


def test_get_family_does_not_translate_repository_failure() -> None:
    class FailingRepository(FamilyRepository):
        def save(self, family: Family) -> None:
            raise RuntimeError("persistence unavailable")

        def get(self, family_id: FamilyId) -> Family | None:
            raise RuntimeError("persistence unavailable")

    family_id = FamilyId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))

    with pytest.raises(RuntimeError, match="persistence unavailable"):
        GetFamily(FailingRepository()).execute(family_id)


def test_get_family_does_not_coerce_non_canonical_identifier() -> None:
    class TypeCheckingRepository(FamilyRepository):
        def save(self, family: Family) -> None:
            raise AssertionError("save must not be called")

        def get(self, family_id: FamilyId) -> Family | None:
            if not isinstance(family_id, FamilyId):
                raise TypeError("family_id must be a FamilyId")
            return None

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        GetFamily(TypeCheckingRepository()).execute(
            cast(FamilyId, "12345678-1234-4234-8234-123456789abc")
        )
