"""Tests for HealthPolicyRegistry."""

import pytest

from familyos_cli.plugins.builtin.health.policies.health_policy import (
    HealthPolicy,
)
from familyos_cli.plugins.builtin.health.policies.health_policy_registry import (
    HealthPolicyRegistry,
)


def create_policy(
    policy_id: str = "health.policy.basic",
) -> HealthPolicy:
    """Create a test health policy."""

    return HealthPolicy(
        id=policy_id,
        name="Basic Health Policy",
        version="1.0.0",
        description="Basic health requirements.",
    )


def test_registry_registers_policy() -> None:
    registry = HealthPolicyRegistry()

    policy = create_policy()

    registry.register(
        policy,
    )

    assert registry.get(
        policy.id,
    ) == policy


def test_registry_returns_none_for_unknown_policy() -> None:
    registry = HealthPolicyRegistry()

    assert registry.get(
        "health.policy.unknown",
    ) is None


def test_registry_lists_registered_policies() -> None:
    registry = HealthPolicyRegistry()

    first = create_policy(
        "health.policy.first",
    )
    second = create_policy(
        "health.policy.second",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.list() == (
        first,
        second,
    )


def test_registry_rejects_duplicate_policy() -> None:
    registry = HealthPolicyRegistry()

    first = create_policy()

    second = HealthPolicy(
        id="health.policy.basic",
        name="Updated Health Policy",
        version="2.0.0",
        description="Updated requirements.",
    )

    registry.register(
        first,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            second,
        )

    assert registry.get(
        "health.policy.basic",
    ) == first
