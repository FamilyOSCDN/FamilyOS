"""Tests for canonical EstablishMembership application semantics."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import (
    EstablishMembership,
    FamilyNotFoundError,
    MembershipConflictError,
    PersonNotFoundError,
)
from familyos_cli.application.ports.family import (
    FamilyRepository,
    MembershipRepository,
)
from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.family import Family, FamilyId, Membership
from familyos_cli.domain.person import Person, PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


class StubFamilyRepository(FamilyRepository):
    def __init__(self, family: Family | None) -> None:
        self.family = family
        self.requested: list[FamilyId] = []

    def save(self, family: Family) -> None:
        self.family = family

    def get(self, family_id: FamilyId) -> Family | None:
        self.requested.append(family_id)
        if self.family is None or self.family.family_id != family_id:
            return None
        return self.family


class StubPersonRepository(PersonRepository):
    def __init__(self, person: Person | None) -> None:
        self.person = person
        self.requested: list[PersonId] = []

    def save(self, person: Person) -> None:
        self.person = person

    def get(self, person_id: PersonId) -> Person | None:
        self.requested.append(person_id)
        if self.person is None or self.person.person_id != person_id:
            return None
        return self.person


class RecordingMembershipRepository(MembershipRepository):
    def __init__(self, existing: Membership | None = None) -> None:
        self.existing = existing
        self.get_requests: list[tuple[FamilyId, PersonId]] = []
        self.saved: list[Membership] = []

    def save(self, membership: Membership) -> None:
        self.saved.append(membership)
        self.existing = membership

    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        self.get_requests.append((family_id, person_id))
        if self.existing is None:
            return None
        if (
            self.existing.family_id != family_id
            or self.existing.person_id != person_id
        ):
            return None
        return self.existing


def _use_case(
    membership_repository: MembershipRepository,
    *,
    family: Family | None = None,
    person: Person | None = None,
    clock=lambda: datetime(2026, 8, 28, 14, 0, tzinfo=UTC),
) -> tuple[EstablishMembership, StubFamilyRepository, StubPersonRepository]:
    family_id = _family_id()
    person_id = _person_id()
    family_repository = StubFamilyRepository(
        Family(family_id=family_id) if family is None else family
    )
    person_repository = StubPersonRepository(
        Person(person_id=person_id) if person is None else person
    )
    return (
        EstablishMembership(
            family_repository,
            person_repository,
            membership_repository,
            clock=clock,
        ),
        family_repository,
        person_repository,
    )


def test_establish_membership_persists_pending_membership_and_returns_event() -> None:
    repository = RecordingMembershipRepository()
    use_case, _, _ = _use_case(repository)
    occurred_at = datetime(2026, 8, 28, 15, 0, tzinfo=UTC)
    use_case._clock = lambda: occurred_at

    result = use_case.execute(_family_id(), _person_id())

    assert repository.saved == [result.membership]
    assert result.membership == Membership.establish(_family_id(), _person_id())
    assert result.event.family_id == _family_id()
    assert result.event.person_id == _person_id()
    assert result.event.occurred_at == occurred_at


def test_establish_membership_uses_clock_once() -> None:
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 28, 15, 30, tzinfo=UTC)

    repository = RecordingMembershipRepository()
    use_case, _, _ = _use_case(repository, clock=clock)

    use_case.execute(_family_id(), _person_id())

    assert calls == 1


def test_establish_membership_rejects_invalid_family_id_before_resolution() -> None:
    repository = RecordingMembershipRepository()
    use_case, family_repository, person_repository = _use_case(repository)

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        use_case.execute(cast(FamilyId, "family-001"), _person_id())

    assert family_repository.requested == []
    assert person_repository.requested == []
    assert repository.get_requests == []
    assert repository.saved == []


def test_establish_membership_rejects_invalid_person_id_before_resolution() -> None:
    repository = RecordingMembershipRepository()
    use_case, family_repository, person_repository = _use_case(repository)

    with pytest.raises(TypeError, match="person_id must be a PersonId"):
        use_case.execute(_family_id(), cast(PersonId, "person-001"))

    assert family_repository.requested == []
    assert person_repository.requested == []
    assert repository.get_requests == []
    assert repository.saved == []


def test_establish_membership_fails_when_family_is_absent() -> None:
    family_repository = StubFamilyRepository(None)
    person_repository = StubPersonRepository(Person(person_id=_person_id()))
    membership_repository = RecordingMembershipRepository()
    use_case = EstablishMembership(
        family_repository,
        person_repository,
        membership_repository,
        clock=lambda: datetime(2026, 8, 28, 16, 0, tzinfo=UTC),
    )

    with pytest.raises(FamilyNotFoundError):
        use_case.execute(_family_id(), _person_id())

    assert person_repository.requested == []
    assert membership_repository.get_requests == []
    assert membership_repository.saved == []


def test_establish_membership_fails_when_person_is_absent() -> None:
    family_repository = StubFamilyRepository(Family(family_id=_family_id()))
    person_repository = StubPersonRepository(None)
    membership_repository = RecordingMembershipRepository()
    use_case = EstablishMembership(
        family_repository,
        person_repository,
        membership_repository,
        clock=lambda: datetime(2026, 8, 28, 16, 30, tzinfo=UTC),
    )

    with pytest.raises(PersonNotFoundError):
        use_case.execute(_family_id(), _person_id())

    assert membership_repository.get_requests == []
    assert membership_repository.saved == []


def test_establish_membership_rejects_existing_continuity_before_clock() -> None:
    existing = Membership.establish(_family_id(), _person_id()).end()
    repository = RecordingMembershipRepository(existing)
    clock_calls = 0

    def clock() -> datetime:
        nonlocal clock_calls
        clock_calls += 1
        return datetime(2026, 8, 28, 17, 0, tzinfo=UTC)

    use_case, _, _ = _use_case(repository, clock=clock)

    with pytest.raises(MembershipConflictError):
        use_case.execute(_family_id(), _person_id())

    assert clock_calls == 0
    assert repository.saved == []


def test_establish_membership_rejects_naive_event_time_before_persistence() -> None:
    repository = RecordingMembershipRepository()
    use_case, _, _ = _use_case(
        repository,
        clock=lambda: datetime(2026, 8, 28, 17, 30),
    )

    with pytest.raises(
        ValueError,
        match="FamilyMembershipCreated occurrence time must be timezone-aware",
    ):
        use_case.execute(_family_id(), _person_id())

    assert repository.saved == []


def test_establish_membership_propagates_clock_failure_before_persistence() -> None:
    repository = RecordingMembershipRepository()

    def failing_clock() -> datetime:
        raise RuntimeError("clock unavailable")

    use_case, _, _ = _use_case(repository, clock=failing_clock)

    with pytest.raises(RuntimeError, match="clock unavailable"):
        use_case.execute(_family_id(), _person_id())

    assert repository.saved == []


def test_establish_membership_propagates_repository_failure() -> None:
    class FailingMembershipRepository(RecordingMembershipRepository):
        def save(self, membership: Membership) -> None:
            raise RuntimeError("persistence unavailable")

    repository = FailingMembershipRepository()
    use_case, _, _ = _use_case(repository)

    with pytest.raises(RuntimeError, match="persistence unavailable"):
        use_case.execute(_family_id(), _person_id())


def test_establish_membership_propagates_family_repository_failure() -> None:
    class FailingFamilyRepository(StubFamilyRepository):
        def get(self, family_id: FamilyId) -> Family | None:
            raise RuntimeError("family persistence unavailable")

    membership_repository = RecordingMembershipRepository()
    use_case = EstablishMembership(
        FailingFamilyRepository(None),
        StubPersonRepository(Person(person_id=_person_id())),
        membership_repository,
        clock=lambda: datetime(2026, 8, 28, 18, 0, tzinfo=UTC),
    )

    with pytest.raises(RuntimeError, match="family persistence unavailable"):
        use_case.execute(_family_id(), _person_id())

    assert membership_repository.saved == []


def test_establish_membership_propagates_person_repository_failure() -> None:
    class FailingPersonRepository(StubPersonRepository):
        def get(self, person_id: PersonId) -> Person | None:
            raise RuntimeError("person persistence unavailable")

    membership_repository = RecordingMembershipRepository()
    use_case = EstablishMembership(
        StubFamilyRepository(Family(family_id=_family_id())),
        FailingPersonRepository(None),
        membership_repository,
        clock=lambda: datetime(2026, 8, 28, 18, 30, tzinfo=UTC),
    )

    with pytest.raises(RuntimeError, match="person persistence unavailable"):
        use_case.execute(_family_id(), _person_id())

    assert membership_repository.saved == []
