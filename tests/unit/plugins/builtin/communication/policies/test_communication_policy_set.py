"""Tests for CommunicationPolicySet."""

import pytest

from familyos_cli.plugins.builtin.communication.policies import (
    CommunicationPolicy,
    CommunicationPolicySet,
)


def create_policy(
    policy_id: str,
) -> CommunicationPolicy:
    return CommunicationPolicy(
        id=policy_id,
        name="Communication Policy",
        version="1.0.0",
    )


def test_communication_policy_set_is_empty_by_default() -> None:
    policy_set = CommunicationPolicySet()

    assert policy_set.list() == ()


def test_communication_policy_set_preserves_order() -> None:
    first = create_policy(
        "communication.policy.first",
    )

    second = create_policy(
        "communication.policy.second",
    )

    policy_set = CommunicationPolicySet(
        policies=(
            first,
            second,
        ),
    )

    assert policy_set.list() == (
        first,
        second,
    )


def test_communication_policy_set_returns_policy_by_id() -> None:
    policy = create_policy(
        "communication.policy.retention",
    )

    policy_set = CommunicationPolicySet(
        policies=(policy,),
    )

    assert policy_set.get(
        "communication.policy.retention",
    ) is policy


def test_communication_policy_set_returns_none_for_unknown_id() -> None:
    policy_set = CommunicationPolicySet()

    assert policy_set.get(
        "communication.policy.unknown",
    ) is None


def test_communication_policy_set_rejects_duplicate_ids() -> None:
    first = create_policy(
        "communication.policy.retention",
    )

    duplicate = create_policy(
        "communication.policy.retention",
    )

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        CommunicationPolicySet(
            policies=(
                first,
                duplicate,
            ),
        )
