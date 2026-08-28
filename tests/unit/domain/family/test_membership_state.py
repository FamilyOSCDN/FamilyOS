"""Tests for canonical Membership lifecycle states."""

from familyos_cli.domain.family import MembershipState


def test_membership_state_contains_only_canonical_initial_states() -> None:
    assert tuple(MembershipState) == (
        MembershipState.PENDING,
        MembershipState.ACTIVE,
        MembershipState.SUSPENDED,
        MembershipState.ENDED,
    )


def test_membership_state_values_are_stable_strings() -> None:
    assert MembershipState.PENDING.value == "pending"
    assert MembershipState.ACTIVE.value == "active"
    assert MembershipState.SUSPENDED.value == "suspended"
    assert MembershipState.ENDED.value == "ended"
