"""Integration tests for canonical Family create/retrieve flow."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from familyos_cli.application.family import (
    CreateFamily,
    FamilyConflictError,
    GetFamily,
)
from familyos_cli.domain.family import FamilyId
from familyos_cli.infrastructure.family import InMemoryFamilyRepository


def test_create_then_get_returns_same_canonical_family() -> None:
    repository = InMemoryFamilyRepository()
    family_id = FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))
    occurred_at = datetime(2026, 8, 28, 14, 0, tzinfo=UTC)

    creation = CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=lambda: occurred_at,
    ).execute()

    retrieved = GetFamily(repository).execute(family_id)

    assert retrieved == creation.family
    assert creation.family.family_id == family_id
    assert creation.event.family_id == family_id
    assert creation.event.occurred_at == occurred_at


def test_get_before_create_returns_none_then_returns_family_after_create() -> None:
    repository = InMemoryFamilyRepository()
    family_id = FamilyId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    get_family = GetFamily(repository)

    assert get_family.execute(family_id) is None

    CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=lambda: datetime(2026, 8, 28, 14, 30, tzinfo=UTC),
    ).execute()

    retrieved = get_family.execute(family_id)

    assert retrieved is not None
    assert retrieved.family_id == family_id


def test_two_creations_with_distinct_ids_remain_independently_retrievable() -> None:
    repository = InMemoryFamilyRepository()
    first_id = FamilyId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))
    second_id = FamilyId(UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))

    CreateFamily(
        repository,
        family_id_factory=lambda: first_id,
        clock=lambda: datetime(2026, 8, 28, 15, 0, tzinfo=UTC),
    ).execute()

    CreateFamily(
        repository,
        family_id_factory=lambda: second_id,
        clock=lambda: datetime(2026, 8, 28, 15, 5, tzinfo=UTC),
    ).execute()

    get_family = GetFamily(repository)
    first = get_family.execute(first_id)
    second = get_family.execute(second_id)

    assert first is not None
    assert second is not None
    assert first.family_id == first_id
    assert second.family_id == second_id
    assert first != second


def test_duplicate_creation_fails_without_replacing_original_family() -> None:
    repository = InMemoryFamilyRepository()
    family_id = FamilyId(UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd"))

    first_result = CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=lambda: datetime(2026, 8, 28, 16, 0, tzinfo=UTC),
    ).execute()

    duplicate_creation = CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=lambda: datetime(2026, 8, 28, 16, 5, tzinfo=UTC),
    )

    with pytest.raises(
        FamilyConflictError,
        match=f"Family '{family_id}' already exists",
    ):
        duplicate_creation.execute()

    assert repository.get(family_id) is first_result.family
