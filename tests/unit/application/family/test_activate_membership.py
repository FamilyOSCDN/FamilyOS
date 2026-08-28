"""Tests for canonical ActivateMembership application semantics."""

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import (
    ActivateMembership,
    MembershipNotFoundError,
)
from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipActivated,
    FamilyMembershipReactivated,
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
        self.requests: list[tuple[FamilyId, PersonId]] = []
        self.saved: list[Membership] = []

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


def test_activate_pending_membership_returns_activated_event() -> None:
    repository = RecordingMembershipRepository(
        Membership.establish(_family_id(), _person_id())
    )
    occurred_at = datetime(2026, 8, 28, 19, 0, tzinfo=UTC)

    result = ActivateMembership(
        repository,
        clock=lambda: occurred_at,
    ).execute(_family_id(), _person_id())

    assert result.membership.state is MembershipState.ACTIVE
    assert isinstance(result.event, FamilyMembershipActivated)
    assert result.event.family_id == _family_id()
    assert result.event.person_id == _person_id()
    assert result.event.occurred_at == occurred_at
    assert repository.saved == [result.membership]


def test_activate_suspended_membership_returns_reactivated_event() -> None:
    suspended = Membership.establish(_family_id(), _person_id()).activate().suspend()
    repository = RecordingMembershipRepository(suspended)

    result = ActivateMembership(
        repository,
        clock=lambda: datetime(2026, 8, 28, 19, 30, tzinfo=UTC),
    ).execute(_family_id(), _person_id())

    assert result.membership.state is MembershipState.ACTIVE
    assert isinstance(result.event, FamilyMembershipReactivated)


def test_activate_preserves_membership_identity() -> None:
    original = Membership.establish(_family_id(), _person_id())
    repository = RecordingMembershipRepository(original)

    result = ActivateMembership(
        repository,
        clock=lambda: datetime(2026, 8, 28, 20, 0, tzinfo=UTC),
    ).execute(_family_id(), _person_id())

    assert result.membership.family_id == original.family_id
    assert result.membership.person_id == original.person_id


def test_activate_rejects_absence_before_clock_and_save() -> None:
    repository = RecordingMembershipRepository(None)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 28, 20, 30, tzinfo=UTC)

    with pytest.raises(MembershipNotFoundError):
        ActivateMembership(repository, clock=clock).execute(
            _family_id(), _person_id()
        )

    assert calls == 0
    assert repository.saved == []


@pytest.mark.parametrize(
    "membership",
    [
        Membership.establish(_family_id(), _person_id()).activate(),
        Membership.establish(_family_id(), _person_id()).end(),
    ],
)
def test_activate_rejects_invalid_source_before_clock_and_save(
    membership: Membership,
) -> None:
    repository = RecordingMembershipRepository(membership)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 28, 21, 0, tzinfo=UTC)

    with pytest.raises(InvalidMembershipTransitionError):
        ActivateMembership(repository, clock=clock).execute(
            _family_id(), _person_id()
        )

    assert calls == 0
    assert repository.saved == []


def test_activate_rejects_naive_event_time_before_save() -> None:
    repository = RecordingMembershipRepository(
        Membership.establish(_family_id(), _person_id())
    )

    with pytest.raises(
        ValueError,
        match="FamilyMembershipActivated occurrence time must be timezone-aware",
    ):
        ActivateMembership(
            repository,
            clock=lambda: datetime(2026, 8, 28, 21, 30),
        ).execute(_family_id(), _person_id())

    assert repository.saved == []


def test_activate_uses_clock_once() -> None:
    repository = RecordingMembershipRepository(
        Membership.establish(_family_id(), _person_id())
    )
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 28, 22, 0, tzinfo=UTC)

    ActivateMembership(repository, clock=clock).execute(
        _family_id(), _person_id()
    )

    assert calls == 1


def test_activate_propagates_save_conflict() -> None:
    class ConflictingRepository(RecordingMembershipRepository):
        def save(self, membership: Membership, temporal_fact: object) -> None:
            raise MembershipConflictError("concurrent Membership transition")

    repository = ConflictingRepository(
        Membership.establish(_family_id(), _person_id())
    )

    with pytest.raises(
        MembershipConflictError,
        match="concurrent Membership transition",
    ):
        ActivateMembership(
            repository,
            clock=lambda: datetime(2026, 8, 28, 22, 30, tzinfo=UTC),
        ).execute(_family_id(), _person_id())


def test_activate_propagates_repository_get_failure() -> None:
    class FailingRepository(RecordingMembershipRepository):
        def get(
            self,
            family_id: FamilyId,
            person_id: PersonId,
        ) -> Membership | None:
            raise RuntimeError("persistence unavailable")

    with pytest.raises(RuntimeError, match="persistence unavailable"):
        ActivateMembership(
            FailingRepository(None),
            clock=lambda: datetime(2026, 8, 28, 23, 0, tzinfo=UTC),
        ).execute(_family_id(), _person_id())


def test_activate_rejects_invalid_identifiers_before_repository_access() -> None:
    repository = RecordingMembershipRepository(None)

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        ActivateMembership(
            repository,
            clock=lambda: datetime(2026, 8, 28, 23, 30, tzinfo=UTC),
        ).execute(cast(FamilyId, "family-001"), _person_id())

    with pytest.raises(TypeError, match="person_id must be a PersonId"):
        ActivateMembership(
            repository,
            clock=lambda: datetime(2026, 8, 28, 23, 30, tzinfo=UTC),
        ).execute(_family_id(), cast(PersonId, "person-001"))

    assert repository.requests == []
