"""Tests for canonical Family Membership semantics."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import (
    FamilyId,
    InvalidMembershipTransitionError,
    Membership,
    MembershipState,
)
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


def _membership(state: MembershipState) -> Membership:
    return Membership(
        family_id=_family_id(),
        person_id=_person_id(),
        state=state,
    )


def test_membership_requires_canonical_family_id() -> None:
    with pytest.raises(TypeError, match="Membership family_id must be a FamilyId"):
        Membership(
            family_id=cast(FamilyId, "family-001"),
            person_id=_person_id(),
            state=MembershipState.PENDING,
        )


def test_membership_requires_canonical_person_id() -> None:
    with pytest.raises(TypeError, match="Membership person_id must be a PersonId"):
        Membership(
            family_id=_family_id(),
            person_id=cast(PersonId, "person-001"),
            state=MembershipState.PENDING,
        )


def test_membership_requires_canonical_state() -> None:
    with pytest.raises(TypeError, match="Membership state must be a MembershipState"):
        Membership(
            family_id=_family_id(),
            person_id=_person_id(),
            state=cast(MembershipState, "active"),
        )


def test_membership_is_immutable() -> None:
    membership = _membership(MembershipState.PENDING)

    with pytest.raises(FrozenInstanceError):
        membership.state = MembershipState.ACTIVE  # type: ignore[misc]


def test_establish_creates_pending_membership_with_composite_identity() -> None:
    family_id = _family_id()
    person_id = _person_id()

    membership = Membership.establish(family_id, person_id)

    assert membership.family_id == family_id
    assert membership.person_id == person_id
    assert membership.state is MembershipState.PENDING


@pytest.mark.parametrize(
    ("source", "expected_validity"),
    [
        (MembershipState.PENDING, False),
        (MembershipState.ACTIVE, True),
        (MembershipState.SUSPENDED, False),
        (MembershipState.ENDED, False),
    ],
)
def test_current_business_validity_requires_active(
    source: MembershipState,
    expected_validity: bool,
) -> None:
    assert _membership(source).is_currently_valid is expected_validity


@pytest.mark.parametrize(
    "source",
    [MembershipState.PENDING, MembershipState.SUSPENDED],
)
def test_activate_preserves_identity_and_returns_active_membership(
    source: MembershipState,
) -> None:
    original = _membership(source)

    transitioned = original.activate()

    assert transitioned is not original
    assert transitioned.family_id == original.family_id
    assert transitioned.person_id == original.person_id
    assert transitioned.state is MembershipState.ACTIVE
    assert original.state is source


@pytest.mark.parametrize(
    "source",
    [MembershipState.ACTIVE, MembershipState.ENDED],
)
def test_activate_rejects_non_canonical_source_states(
    source: MembershipState,
) -> None:
    membership = _membership(source)

    with pytest.raises(
        InvalidMembershipTransitionError,
        match=rf"{source.value} -> active",
    ):
        membership.activate()


def test_suspend_transitions_active_to_suspended_and_preserves_identity() -> None:
    original = _membership(MembershipState.ACTIVE)

    transitioned = original.suspend()

    assert transitioned.family_id == original.family_id
    assert transitioned.person_id == original.person_id
    assert transitioned.state is MembershipState.SUSPENDED
    assert original.state is MembershipState.ACTIVE


@pytest.mark.parametrize(
    "source",
    [
        MembershipState.PENDING,
        MembershipState.SUSPENDED,
        MembershipState.ENDED,
    ],
)
def test_suspend_rejects_non_active_source_states(source: MembershipState) -> None:
    membership = _membership(source)

    with pytest.raises(
        InvalidMembershipTransitionError,
        match=rf"{source.value} -> suspended",
    ):
        membership.suspend()


@pytest.mark.parametrize(
    "source",
    [
        MembershipState.PENDING,
        MembershipState.ACTIVE,
        MembershipState.SUSPENDED,
    ],
)
def test_end_transitions_every_authorized_source_to_ended(
    source: MembershipState,
) -> None:
    original = _membership(source)

    transitioned = original.end()

    assert transitioned.family_id == original.family_id
    assert transitioned.person_id == original.person_id
    assert transitioned.state is MembershipState.ENDED
    assert original.state is source


def test_ended_is_terminal() -> None:
    ended = _membership(MembershipState.ENDED)

    with pytest.raises(
        InvalidMembershipTransitionError,
        match=r"ended -> ended",
    ):
        ended.end()

    with pytest.raises(
        InvalidMembershipTransitionError,
        match=r"ended -> active",
    ):
        ended.activate()

    with pytest.raises(
        InvalidMembershipTransitionError,
        match=r"ended -> suspended",
    ):
        ended.suspend()


def test_composite_identity_remains_unchanged_across_full_nonterminal_lifecycle() -> None:
    pending = Membership.establish(_family_id(), _person_id())
    active = pending.activate()
    suspended = active.suspend()
    reactivated = suspended.activate()
    ended = reactivated.end()

    expected_key = (pending.family_id, pending.person_id)

    assert (active.family_id, active.person_id) == expected_key
    assert (suspended.family_id, suspended.person_id) == expected_key
    assert (reactivated.family_id, reactivated.person_id) == expected_key
    assert (ended.family_id, ended.person_id) == expected_key


def test_membership_has_no_dedicated_membership_identifier() -> None:
    membership = Membership.establish(_family_id(), _person_id())

    assert set(membership.__dataclass_fields__) == {
        "family_id",
        "person_id",
        "state",
    }
