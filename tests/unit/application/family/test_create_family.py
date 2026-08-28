"""Tests for canonical CreateFamily application semantics."""

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import CreateFamily, FamilyConflictError
from familyos_cli.application.ports.family import FamilyRepository
from familyos_cli.domain.family import Family, FamilyId


class RecordingFamilyRepository(FamilyRepository):
    """Minimal repository test double recording canonical saves."""

    def __init__(self) -> None:
        self.saved: list[Family] = []

    def save(self, family: Family) -> None:
        self.saved.append(family)

    def get(self, family_id: FamilyId) -> Family | None:
        return next(
            (family for family in self.saved if family.family_id == family_id),
            None,
        )


def test_create_family_persists_exactly_one_family_and_returns_event() -> None:
    repository = RecordingFamilyRepository()
    family_id = FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))
    occurred_at = datetime(2026, 8, 28, 10, 0, tzinfo=UTC)

    use_case = CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=lambda: occurred_at,
    )

    result = use_case.execute()

    assert repository.saved == [result.family]
    assert result.family.family_id == family_id
    assert result.event.family_id == family_id
    assert result.event.occurred_at == occurred_at


def test_create_family_uses_injected_identity_factory_once() -> None:
    repository = RecordingFamilyRepository()
    family_id = FamilyId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    calls = 0

    def generate_family_id() -> FamilyId:
        nonlocal calls
        calls += 1
        return family_id

    result = CreateFamily(
        repository,
        family_id_factory=generate_family_id,
        clock=lambda: datetime(2026, 8, 28, 10, 30, tzinfo=UTC),
    ).execute()

    assert calls == 1
    assert result.family.family_id == family_id


def test_create_family_uses_injected_clock_once() -> None:
    repository = RecordingFamilyRepository()
    occurred_at = datetime(2026, 8, 28, 11, 0, tzinfo=UTC)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return occurred_at

    result = CreateFamily(repository, clock=clock).execute()

    assert calls == 1
    assert result.event.occurred_at == occurred_at


def test_create_family_rejects_invalid_identity_before_clock_and_persistence() -> None:
    repository = RecordingFamilyRepository()
    clock_calls = 0

    def clock() -> datetime:
        nonlocal clock_calls
        clock_calls += 1
        return datetime(2026, 8, 28, 11, 30, tzinfo=UTC)

    use_case = CreateFamily(
        repository,
        family_id_factory=lambda: cast(FamilyId, "family-001"),
        clock=clock,
    )

    with pytest.raises(TypeError, match="Family family_id must be a FamilyId"):
        use_case.execute()

    assert repository.saved == []
    assert clock_calls == 0


def test_create_family_propagates_identity_factory_failure() -> None:
    repository = RecordingFamilyRepository()

    def failing_family_id_factory() -> FamilyId:
        raise RuntimeError("identity generation unavailable")

    use_case = CreateFamily(
        repository,
        family_id_factory=failing_family_id_factory,
        clock=lambda: datetime(2026, 8, 28, 12, 0, tzinfo=UTC),
    )

    with pytest.raises(RuntimeError, match="identity generation unavailable"):
        use_case.execute()

    assert repository.saved == []


def test_create_family_propagates_clock_failure_before_persistence() -> None:
    repository = RecordingFamilyRepository()
    family_id = FamilyId(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))

    def failing_clock() -> datetime:
        raise RuntimeError("clock unavailable")

    use_case = CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=failing_clock,
    )

    with pytest.raises(RuntimeError, match="clock unavailable"):
        use_case.execute()

    assert repository.saved == []


def test_create_family_rejects_naive_occurrence_time_before_persistence() -> None:
    repository = RecordingFamilyRepository()
    family_id = FamilyId(UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))

    use_case = CreateFamily(
        repository,
        family_id_factory=lambda: family_id,
        clock=lambda: datetime(2026, 8, 28, 12, 30),
    )

    with pytest.raises(
        ValueError,
        match="FamilyCreated occurrence time must be timezone-aware",
    ):
        use_case.execute()

    assert repository.saved == []


def test_create_family_propagates_family_conflict() -> None:
    class ConflictingRepository(FamilyRepository):
        def save(self, family: Family) -> None:
            raise FamilyConflictError(f"Family '{family.family_id}' already exists")

        def get(self, family_id: FamilyId) -> Family | None:
            return None

    family_id = FamilyId(UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd"))
    use_case = CreateFamily(
        ConflictingRepository(),
        family_id_factory=lambda: family_id,
        clock=lambda: datetime(2026, 8, 28, 13, 0, tzinfo=UTC),
    )

    with pytest.raises(
        FamilyConflictError,
        match=f"Family '{family_id}' already exists",
    ):
        use_case.execute()


def test_create_family_propagates_repository_failure() -> None:
    class FailingRepository(FamilyRepository):
        def save(self, family: Family) -> None:
            raise RuntimeError("persistence unavailable")

        def get(self, family_id: FamilyId) -> Family | None:
            return None

    family_id = FamilyId(UUID("eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"))
    use_case = CreateFamily(
        FailingRepository(),
        family_id_factory=lambda: family_id,
        clock=lambda: datetime(2026, 8, 28, 13, 30, tzinfo=UTC),
    )

    with pytest.raises(RuntimeError, match="persistence unavailable"):
        use_case.execute()
