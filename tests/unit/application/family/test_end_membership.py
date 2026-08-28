"""Tests for canonical EndMembership application semantics."""

from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.application.family import EndMembership, MembershipNotFoundError
from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipEnded,
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


@pytest.mark.parametrize(
    "membership",
    [
        Membership.establish(_family_id(), _person_id()),
        Membership.establish(_family_id(), _person_id()).activate(),
        Membership.establish(_family_id(), _person_id()).activate().suspend(),
    ],
)
def test_end_allows_every_non_terminal_source(membership: Membership) -> None:
    repository = RecordingMembershipRepository(membership)
    occurred_at = datetime(2026, 8, 29, 4, 0, tzinfo=UTC)

    result = EndMembership(
        repository,
        clock=lambda: occurred_at,
    ).execute(_family_id(), _person_id())

    assert result.membership.state is MembershipState.ENDED
    assert result.membership.family_id == membership.family_id
    assert result.membership.person_id == membership.person_id
    assert isinstance(result.event, FamilyMembershipEnded)
    assert result.event.occurred_at == occurred_at
    assert repository.saved == [result.membership]


def test_end_rejects_ended_before_clock_and_save() -> None:
    ended = Membership.establish(_family_id(), _person_id()).end()
    repository = RecordingMembershipRepository(ended)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 29, 4, 30, tzinfo=UTC)

    with pytest.raises(InvalidMembershipTransitionError):
        EndMembership(repository, clock=clock).execute(
            _family_id(), _person_id()
        )

    assert calls == 0
    assert repository.saved == []


def test_end_rejects_absence_before_clock_and_save() -> None:
    repository = RecordingMembershipRepository(None)
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 29, 5, 0, tzinfo=UTC)

    with pytest.raises(MembershipNotFoundError):
        EndMembership(repository, clock=clock).execute(
            _family_id(), _person_id()
        )

    assert calls == 0
    assert repository.saved == []


def test_end_rejects_naive_event_time_before_save() -> None:
    repository = RecordingMembershipRepository(
        Membership.establish(_family_id(), _person_id())
    )

    with pytest.raises(
        ValueError,
        match="FamilyMembershipEnded occurrence time must be timezone-aware",
    ):
        EndMembership(
            repository,
            clock=lambda: datetime(2026, 8, 29, 5, 30),
        ).execute(_family_id(), _person_id())

    assert repository.saved == []


def test_end_uses_clock_once() -> None:
    repository = RecordingMembershipRepository(
        Membership.establish(_family_id(), _person_id())
    )
    calls = 0

    def clock() -> datetime:
        nonlocal calls
        calls += 1
        return datetime(2026, 8, 29, 6, 0, tzinfo=UTC)

    EndMembership(repository, clock=clock).execute(
        _family_id(), _person_id()
    )

    assert calls == 1


def test_end_propagates_save_conflict() -> None:
    class ConflictingRepository(RecordingMembershipRepository):
        def save(self, membership: Membership, temporal_fact: object) -> None:
            raise MembershipConflictError("concurrent Membership transition")

    repository = ConflictingRepository(
        Membership.establish(_family_id(), _person_id())
    )

    with pytest.raises(MembershipConflictError):
        EndMembership(
            repository,
            clock=lambda: datetime(2026, 8, 29, 6, 30, tzinfo=UTC),
        ).execute(_family_id(), _person_id())


def test_end_rejects_invalid_identifiers_before_repository_access() -> None:
    repository = RecordingMembershipRepository(None)
    command = EndMembership(
        repository,
        clock=lambda: datetime(2026, 8, 29, 7, 0, tzinfo=UTC),
    )

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        command.execute(cast(FamilyId, "family-001"), _person_id())

    with pytest.raises(TypeError, match="person_id must be a PersonId"):
        command.execute(_family_id(), cast(PersonId, "person-001"))

    assert repository.requests == []
