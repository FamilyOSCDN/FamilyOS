"""Tests for canonical SuspendMembership application semantics."""

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import (
    MembershipNotFoundError,
    SuspendMembership,
)
from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipSuspended,
    InvalidMembershipTransitionError,
    Membership,
    MembershipState,
)
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


class RecordingMembershipRepository(MembershipRepository):
    def __init__(self, membership: Membership | None) -> None:
        self.membership = membership
        self.saved: list[Membership] = []
        self.requests: list[tuple[FamilyId, PersonId]] = []

    def save(self, membership: Membership, temporal_fact: object) -> None:
        self.saved.append(membership)
        self.membership = membership

    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        self.requests.append((family_id, person_id))
        return self.membership


def test_suspend_active_membership_returns_suspended_event() -> None:
    active = Membership.establish(_family_id(), _person_id()).activate()
    repository = RecordingMembershipRepository(active)
    occurred_at = datetime(2026, 8, 29, 0, 0, tzinfo=UTC)

    result = SuspendMembership(
        repository,
        clock=lambda: occurred_at,
    ).execute(_family_id(), _person_id())

    assert result.membership.state is MembershipState.SUSPENDED
    assert isinstance(result.event, FamilyMembershipSuspended)
    assert result.event.occurred_at == occurred_at
    assert repository.saved == [result.membership]


@pytest.mark.parametrize(
    "membership",
    [
        Membership.establish(_family_id(), _person_id()),
        Membership.establish(_family_id(), _person_id()).activate().suspend(),
        Membership.establish(_family_id(), _person_id()).end(),
    ],
)
def test_suspend_rejects_invalid_source_before_clock_and_save(
    membership: Membership,
) -> None:
    repository = RecordingMembershipRepository(membership)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 29, 0, 30, tzinfo=UTC)

    with pytest.raises(InvalidMembershipTransitionError):
        SuspendMembership(repository, clock=clock).execute(
            _family_id(), _person_id()
        )

    assert calls == 0
    assert repository.saved == []


def test_suspend_rejects_absence_before_clock_and_save() -> None:
    repository = RecordingMembershipRepository(None)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 29, 1, 0, tzinfo=UTC)

    with pytest.raises(MembershipNotFoundError):
        SuspendMembership(repository, clock=clock).execute(
            _family_id(), _person_id()
        )

    assert calls == 0
    assert repository.saved == []


def test_suspend_rejects_naive_event_time_before_save() -> None:
    active = Membership.establish(_family_id(), _person_id()).activate()
    repository = RecordingMembershipRepository(active)

    with pytest.raises(
        ValueError,
        match="FamilyMembershipSuspended occurrence time must be timezone-aware",
    ):
        SuspendMembership(
            repository,
            clock=lambda: datetime(2026, 8, 29, 1, 30),
        ).execute(_family_id(), _person_id())

    assert repository.saved == []


def test_suspend_preserves_identity_and_uses_clock_once() -> None:
    active = Membership.establish(_family_id(), _person_id()).activate()
    repository = RecordingMembershipRepository(active)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 29, 2, 0, tzinfo=UTC)

    result = SuspendMembership(repository, clock=clock).execute(
        _family_id(), _person_id()
    )

    assert calls == 1
    assert result.membership.family_id == active.family_id
    assert result.membership.person_id == active.person_id


def test_suspend_propagates_save_conflict() -> None:
    class ConflictingRepository(RecordingMembershipRepository):
        def save(self, membership: Membership, temporal_fact: object) -> None:
            raise MembershipConflictError("concurrent Membership transition")

    active = Membership.establish(_family_id(), _person_id()).activate()

    with pytest.raises(MembershipConflictError):
        SuspendMembership(
            ConflictingRepository(active),
            clock=lambda: datetime(2026, 8, 29, 2, 30, tzinfo=UTC),
        ).execute(_family_id(), _person_id())


def test_suspend_rejects_invalid_identifiers_before_repository_access() -> None:
    repository = RecordingMembershipRepository(None)
    command = SuspendMembership(
        repository,
        clock=lambda: datetime(2026, 8, 29, 3, 0, tzinfo=UTC),
    )

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        command.execute(cast(FamilyId, "family-001"), _person_id())

    with pytest.raises(TypeError, match="person_id must be a PersonId"):
        command.execute(_family_id(), cast(PersonId, "person-001"))

    assert repository.requests == []
