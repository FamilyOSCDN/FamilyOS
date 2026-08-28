"""Tests for the in-memory Family repository adapter."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    FamilyConflictError,
    FamilyRepository,
)
from familyos_cli.domain.family import Family, FamilyId
from familyos_cli.infrastructure.family import InMemoryFamilyRepository


def test_repository_implements_canonical_port() -> None:
    repository = InMemoryFamilyRepository()

    assert isinstance(repository, FamilyRepository)


def test_save_then_get_returns_same_canonical_family() -> None:
    family_id = FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))
    family = Family(family_id=family_id)
    repository = InMemoryFamilyRepository()

    repository.save(family)

    assert repository.get(family_id) == family


def test_get_returns_none_for_absent_family() -> None:
    repository = InMemoryFamilyRepository()
    family_id = FamilyId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))

    assert repository.get(family_id) is None


def test_save_rejects_established_identity_without_replacing_family() -> None:
    family_id = FamilyId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))
    first = Family(family_id=family_id)
    second = Family(family_id=family_id)
    repository = InMemoryFamilyRepository()

    repository.save(first)

    with pytest.raises(
        FamilyConflictError,
        match=f"Family '{family_id}' already exists",
    ):
        repository.save(second)

    assert repository.get(family_id) is first


def test_concurrent_save_establishes_identity_exactly_once() -> None:
    family_id = FamilyId(UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))
    families = tuple(Family(family_id=family_id) for _ in range(8))
    barrier = Barrier(len(families))
    repository = InMemoryFamilyRepository()

    def attempt_save(family: Family) -> bool:
        barrier.wait()

        try:
            repository.save(family)
        except FamilyConflictError:
            return False

        return True

    with ThreadPoolExecutor(max_workers=len(families)) as executor:
        outcomes = tuple(executor.map(attempt_save, families))

    assert outcomes.count(True) == 1
    assert outcomes.count(False) == len(families) - 1
    assert repository.get(family_id) is families[outcomes.index(True)]
