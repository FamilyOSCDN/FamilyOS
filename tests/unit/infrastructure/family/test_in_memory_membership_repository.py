"""Tests for atomic in-memory Membership temporal persistence."""

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from threading import Barrier
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
    MembershipTemporalFact,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipActivated,
    FamilyMembershipCreated,
    FamilyMembershipEnded,
    FamilyMembershipReactivated,
    FamilyMembershipSuspended,
    Membership,
    MembershipState,
)
from familyos_cli.domain.person import PersonId
from familyos_cli.infrastructure.family import InMemoryMembershipRepository


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


def _key(membership: Membership) -> tuple[FamilyId, PersonId]:
    return membership.family_id, membership.person_id


def _time(minute: int = 0) -> datetime:
    return datetime(2026, 8, 28, 10, minute, tzinfo=UTC)


def _created(membership: Membership, minute: int = 0) -> FamilyMembershipCreated:
    return FamilyMembershipCreated(
        membership.family_id,
        membership.person_id,
        _time(minute),
    )


def _activated(membership: Membership, minute: int = 1) -> FamilyMembershipActivated:
    return FamilyMembershipActivated(
        membership.family_id,
        membership.person_id,
        _time(minute),
    )


def _suspended(membership: Membership, minute: int = 2) -> FamilyMembershipSuspended:
    return FamilyMembershipSuspended(
        membership.family_id,
        membership.person_id,
        _time(minute),
    )


def _reactivated(
    membership: Membership, minute: int = 3
) -> FamilyMembershipReactivated:
    return FamilyMembershipReactivated(
        membership.family_id,
        membership.person_id,
        _time(minute),
    )


def _ended(membership: Membership, minute: int = 4) -> FamilyMembershipEnded:
    return FamilyMembershipEnded(
        membership.family_id,
        membership.person_id,
        _time(minute),
    )


def _persist_to_state(
    repository: InMemoryMembershipRepository,
    state: MembershipState,
) -> Membership:
    pending = Membership.establish(_family_id(), _person_id())
    repository.save(pending, _created(pending))

    if state is MembershipState.PENDING:
        return pending

    if state is MembershipState.ACTIVE:
        active = pending.activate()
        repository.save(active, _activated(active))
        return active

    if state is MembershipState.SUSPENDED:
        active = pending.activate()
        repository.save(active, _activated(active))
        suspended = active.suspend()
        repository.save(suspended, _suspended(suspended))
        return suspended

    ended = pending.end()
    repository.save(ended, _ended(ended))
    return ended


def _fact_for_valid_successor(
    existing: Membership,
    candidate: Membership,
) -> MembershipTemporalFact:
    if existing.state is MembershipState.PENDING:
        if candidate.state is MembershipState.ACTIVE:
            return _activated(candidate)
        return _ended(candidate)
    if existing.state is MembershipState.ACTIVE:
        if candidate.state is MembershipState.SUSPENDED:
            return _suspended(candidate)
        return _ended(candidate)
    if existing.state is MembershipState.SUSPENDED:
        if candidate.state is MembershipState.ACTIVE:
            return _reactivated(candidate)
        return _ended(candidate)
    raise AssertionError("ENDED has no canonical successor")


def test_repository_implements_canonical_port() -> None:
    assert isinstance(InMemoryMembershipRepository(), MembershipRepository)


def test_initial_pending_save_then_get_returns_membership() -> None:
    membership = Membership.establish(_family_id(), _person_id())
    repository = InMemoryMembershipRepository()

    repository.save(membership, _created(membership))

    assert repository.get(*_key(membership)) == membership


def test_get_returns_none_for_absent_membership() -> None:
    repository = InMemoryMembershipRepository()

    assert repository.get(_family_id(), _person_id()) is None


@pytest.mark.parametrize(
    "state",
    [MembershipState.ACTIVE, MembershipState.SUSPENDED, MembershipState.ENDED],
)
def test_initial_save_rejects_non_pending_state(state: MembershipState) -> None:
    membership = Membership(_family_id(), _person_id(), state)
    repository = InMemoryMembershipRepository()

    with pytest.raises(
        MembershipConflictError,
        match="Initial Membership persistence requires PENDING state",
    ):
        repository.save(membership, _created(membership))

    assert repository.get(*_key(membership)) is None
    assert _key(membership) not in repository._temporal_facts


def test_duplicate_pending_save_is_conflict_and_does_not_replace() -> None:
    first = Membership.establish(_family_id(), _person_id())
    second = Membership.establish(first.family_id, first.person_id)
    repository = InMemoryMembershipRepository()

    repository.save(first, _created(first))

    with pytest.raises(MembershipConflictError):
        repository.save(second, _created(second, 1))

    assert repository.get(*_key(first)) is first
    assert repository._temporal_facts[_key(first)] == (_created(first),)


@pytest.mark.parametrize(
    ("source", "transition"),
    [
        (MembershipState.PENDING, "activate"),
        (MembershipState.PENDING, "end"),
        (MembershipState.ACTIVE, "suspend"),
        (MembershipState.ACTIVE, "end"),
        (MembershipState.SUSPENDED, "activate"),
        (MembershipState.SUSPENDED, "end"),
    ],
)
def test_save_accepts_only_canonical_lifecycle_successor(
    source: MembershipState,
    transition: str,
) -> None:
    repository = InMemoryMembershipRepository()
    current = _persist_to_state(repository, source)

    if transition == "activate":
        successor = current.activate()
    elif transition == "suspend":
        successor = current.suspend()
    else:
        successor = current.end()

    event = _fact_for_valid_successor(current, successor)
    repository.save(successor, event)

    assert repository.get(*_key(current)) == successor
    assert repository._temporal_facts[_key(current)][-1] == event


def test_ended_membership_remains_present_and_key_reserved() -> None:
    repository = InMemoryMembershipRepository()
    pending = Membership.establish(_family_id(), _person_id())
    ended = pending.end()

    repository.save(pending, _created(pending))
    end_event = _ended(ended)
    repository.save(ended, end_event)

    replacement = Membership.establish(pending.family_id, pending.person_id)

    with pytest.raises(MembershipConflictError):
        repository.save(replacement, _created(replacement, 5))

    assert repository.get(*_key(pending)) == ended
    assert repository._temporal_facts[_key(pending)] == (
        _created(pending),
        end_event,
    )


@pytest.mark.parametrize(
    ("existing", "candidate"),
    [
        (MembershipState.PENDING, MembershipState.SUSPENDED),
        (MembershipState.PENDING, MembershipState.PENDING),
        (MembershipState.ACTIVE, MembershipState.PENDING),
        (MembershipState.ACTIVE, MembershipState.ACTIVE),
        (MembershipState.SUSPENDED, MembershipState.PENDING),
        (MembershipState.SUSPENDED, MembershipState.SUSPENDED),
        (MembershipState.ENDED, MembershipState.PENDING),
        (MembershipState.ENDED, MembershipState.ACTIVE),
        (MembershipState.ENDED, MembershipState.SUSPENDED),
        (MembershipState.ENDED, MembershipState.ENDED),
    ],
)
def test_save_rejects_noncanonical_replacement(
    existing: MembershipState,
    candidate: MembershipState,
) -> None:
    repository = InMemoryMembershipRepository()
    current = _persist_to_state(repository, existing)
    before_facts = repository._temporal_facts[_key(current)]

    replacement = Membership(
        family_id=current.family_id,
        person_id=current.person_id,
        state=candidate,
    )

    # Identity and occurrence time are valid. The candidate continuity itself
    # remains non-canonical and must not mutate either stored component.
    fact = _created(replacement, 20)

    with pytest.raises(MembershipConflictError):
        repository.save(replacement, fact)

    assert repository.get(*_key(current)) == current
    assert repository._temporal_facts[_key(current)] == before_facts


def test_initial_save_persists_membership_and_creation_fact() -> None:
    membership = Membership.establish(_family_id(), _person_id())
    event = _created(membership)
    repository = InMemoryMembershipRepository()

    repository.save(membership, event)

    assert repository.get(*_key(membership)) == membership
    assert repository._temporal_facts[_key(membership)] == (event,)


def test_full_lifecycle_preserves_ordered_temporal_facts() -> None:
    repository = InMemoryMembershipRepository()
    pending = Membership.establish(_family_id(), _person_id())
    active = pending.activate()
    suspended = active.suspend()
    reactivated = suspended.activate()
    ended = reactivated.end()
    base = datetime(2026, 8, 28, 11, 0, tzinfo=UTC)

    events = (
        FamilyMembershipCreated(pending.family_id, pending.person_id, base),
        FamilyMembershipActivated(
            pending.family_id,
            pending.person_id,
            base + timedelta(minutes=1),
        ),
        FamilyMembershipSuspended(
            pending.family_id,
            pending.person_id,
            base + timedelta(minutes=2),
        ),
        FamilyMembershipReactivated(
            pending.family_id,
            pending.person_id,
            base + timedelta(minutes=3),
        ),
        FamilyMembershipEnded(
            pending.family_id,
            pending.person_id,
            base + timedelta(minutes=4),
        ),
    )

    repository.save(pending, events[0])
    repository.save(active, events[1])
    repository.save(suspended, events[2])
    repository.save(reactivated, events[3])
    repository.save(ended, events[4])

    assert repository.get(*_key(pending)) == ended
    assert repository._temporal_facts[_key(pending)] == events


def test_temporal_fact_mismatch_is_atomic_conflict() -> None:
    repository = InMemoryMembershipRepository()
    pending = Membership.establish(_family_id(), _person_id())
    created = _created(pending)
    repository.save(pending, created)
    active = pending.activate()
    wrong = _suspended(active)

    with pytest.raises(
        MembershipConflictError,
        match="temporal fact must match canonical lifecycle transition",
    ):
        repository.save(active, wrong)

    assert repository.get(*_key(pending)) == pending
    assert repository._temporal_facts[_key(pending)] == (created,)


def test_temporal_fact_identity_mismatch_is_atomic_conflict() -> None:
    repository = InMemoryMembershipRepository()
    membership = Membership.establish(_family_id(), _person_id())
    wrong = FamilyMembershipCreated(
        FamilyId(UUID("87654321-4321-4321-8321-cba987654321")),
        membership.person_id,
        _time(),
    )

    with pytest.raises(MembershipConflictError, match="must match canonical"):
        repository.save(membership, wrong)

    assert repository.get(*_key(membership)) is None
    assert _key(membership) not in repository._temporal_facts


def test_initial_save_rejects_non_pending_without_persisting_fact() -> None:
    membership = Membership(_family_id(), _person_id(), MembershipState.ACTIVE)
    repository = InMemoryMembershipRepository()

    with pytest.raises(MembershipConflictError):
        repository.save(membership, _created(membership))

    assert repository.get(*_key(membership)) is None
    assert _key(membership) not in repository._temporal_facts


def test_concurrent_initial_save_establishes_composite_identity_exactly_once() -> None:
    family_id = _family_id()
    person_id = _person_id()
    memberships = tuple(Membership.establish(family_id, person_id) for _ in range(8))
    events = tuple(
        _created(membership, index) for index, membership in enumerate(memberships)
    )
    barrier = Barrier(len(memberships))
    repository = InMemoryMembershipRepository()

    def attempt_save(
        item: tuple[Membership, FamilyMembershipCreated],
    ) -> bool:
        membership, event = item
        barrier.wait()
        try:
            repository.save(membership, event)
        except MembershipConflictError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=len(memberships)) as executor:
        outcomes = tuple(
            executor.map(
                attempt_save,
                zip(memberships, events, strict=True),
            )
        )

    assert outcomes.count(True) == 1
    assert outcomes.count(False) == len(memberships) - 1
    winner = outcomes.index(True)
    assert repository.get(family_id, person_id) is memberships[winner]
    assert repository._temporal_facts[(family_id, person_id)] == (events[winner],)


def test_concurrent_initial_save_establishes_identity_and_fact_exactly_once() -> None:
    # Explicit F4.11 atomicity assertion retained in addition to the historical
    # concurrency contract above.
    test_concurrent_initial_save_establishes_composite_identity_exactly_once()
