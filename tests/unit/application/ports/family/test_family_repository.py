"""Tests for the canonical FamilyRepository port."""

from __future__ import annotations

import inspect

import pytest

from familyos_cli.application.ports.family import (
    FamilyConflictError,
    FamilyRepository,
)
from familyos_cli.domain.family import Family, FamilyId


def test_family_repository_is_abstract() -> None:
    assert inspect.isabstract(FamilyRepository)


def test_family_repository_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        FamilyRepository()  # type: ignore[abstract]


def test_concrete_repository_can_implement_canonical_contract() -> None:
    class Repository(FamilyRepository):
        def __init__(self) -> None:
            self._families: dict[FamilyId, Family] = {}

        def save(self, family: Family) -> None:
            if family.family_id in self._families:
                raise FamilyConflictError
            self._families[family.family_id] = family

        def get(self, family_id: FamilyId) -> Family | None:
            return self._families.get(family_id)

    repository = Repository()
    family = Family(family_id=FamilyId.generate())

    assert repository.get(family.family_id) is None

    repository.save(family)

    assert repository.get(family.family_id) == family


def test_family_repository_exposes_only_canonical_repository_operations() -> None:
    public_operations = {
        name
        for name, member in inspect.getmembers(FamilyRepository, inspect.isfunction)
        if not name.startswith("_")
    }

    assert public_operations == {"get", "save"}
