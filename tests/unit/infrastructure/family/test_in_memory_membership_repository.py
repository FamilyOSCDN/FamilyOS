"""Tests for the in-memory Membership repository adapter."""

from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    MembershipConflictError,
    MembershipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
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


def test_repository_implements_canonical_port() -> None:
    assert isinstance(InMemoryMembershipRepository(), MembershipRepository)


def test_initial_pending_save_then_get_returns_membership() -> None:
    membership = Membership.establish(_family_id(), _person_id())
    repository = InMemoryMembershipRepository()

    repository.save(membership)

    assert repository.get(*_key(membership)) == membership


def test_get_returns_none_for_absent_membership() -> None:
    repository = InMemoryMembershipRepository()

    assert repository.get(_family_id(), _person_id()) is None


@pytest.mark.parametrize(
    "state",
    [
        MembershipState.ACTIVE,
        MembershipState.SUSPENDED,
        MembershipState.ENDED,
    ],
)
def test_initial_save_rejects_non_pending_state(state: MembershipState) -> None:
    membership = Membership(
        family_id=_family_id(),
        person_id=_person_id(),
        state=state,
    )
    repository = InMemoryMembershipRepository()

    with pytest.raises(
        MembershipConflictError,
        match="Initial Membership persistence requires PENDING state",
    ):
        repository.save(membership)

    assert repository.get(*_key(membership)) is None


def test_duplicate_pending_save_is_conflict_and_does_not_replace() -> None:
    first = Membership.establish(_family_id(), _person_id())
    second = Membership.establish(first.family_id, first.person_id)
    repository = InMemoryMembershipRepository()

    repository.save(first)

    with pytest.raises(MembershipConflictError):
        repository.save(second)

    assert repository.get(*_key(first)) is first


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
    initial = Membership.establish(_family_id(), _person_id())
    repository.save(initial)

    current = initial
    if source is MembershipState.ACTIVE:
        current = initial.activate()
        repository.save(current)
    elif source is MembershipState.SUSPENDED:
        active = initial.activate()
        repository.save(active)
        current = active.suspend()
        repository.save(current)

    if transition == "activate":
        successor = current.activate()
    elif transition == "suspend":
        successor = current.suspend()
    else:
        successor = current.end()

    repository.save(successor)

    assert repository.get(*_key(initial)) == successor


def test_ended_membership_remains_present_and_key_reserved() -> None:
    repository = InMemoryMembershipRepository()
    pending = Membership.establish(_family_id(), _person_id())
    ended = pending.end()

    repository.save(pending)
    repository.save(ended)

    assert repository.get(*_key(pending)) == ended

    replacement = Membership.establish(pending.family_id, pending.person_id)

    with pytest.raises(MembershipConflictError):
        repository.save(replacement)

    assert repository.get(*_key(pending)) == ended


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
    pending = Membership.establish(_family_id(), _person_id())
    repository.save(pending)

    current = pending
    if existing is MembershipState.ACTIVE:
        current = pending.activate()
        repository.save(current)
    elif existing is MembershipState.SUSPENDED:
        active = pending.activate()
        repository.save(active)
        current = active.suspend()
        repository.save(current)
    elif existing is MembershipState.ENDED:
        current = pending.end()
        repository.save(current)

    replacement = Membership(
        family_id=current.family_id,
        person_id=current.person_id,
        state=candidate,
    )

    with pytest.raises(
        MembershipConflictError,
        match="Membership persistence must preserve one canonical continuity",
    ):
        repository.save(replacement)

    assert repository.get(*_key(current)) == current


def test_concurrent_initial_save_establishes_composite_identity_exactly_once() -> None:
    family_id = _family_id()
    person_id = _person_id()
    memberships = tuple(
        Membership.establish(family_id, person_id)
        for _ in range(8)
    )
    barrier = Barrier(len(memberships))
    repository = InMemoryMembershipRepository()

    def attempt_save(membership: Membership) -> bool:
        barrier.wait()

        try:
            repository.save(membership)
        except MembershipConflictError:
            return False

        return True

    with ThreadPoolExecutor(max_workers=len(memberships)) as executor:
        outcomes = tuple(executor.map(attempt_save, memberships))

    assert outcomes.count(True) == 1
    assert outcomes.count(False) == len(memberships) - 1

    stored = repository.get(family_id, person_id)
    assert stored is memberships[outcomes.index(True)]
