"""Tests for FinancePolicyRegistry."""

from familyos_cli.plugins.builtin.finance.policies.finance_policy import (
    FinancePolicy,
)
from familyos_cli.plugins.builtin.finance.policies.finance_policy_registry import (
    FinancePolicyRegistry,
)


def create_policy(
    policy_id: str = "finance.policy.basic",
) -> FinancePolicy:
    """Create a test finance policy."""

    return FinancePolicy(
        id=policy_id,
        name="Basic Finance Policy",
        version="1.0.0",
        description="Basic finance requirements.",
    )


def test_registry_registers_policy() -> None:
    registry = FinancePolicyRegistry()

    policy = create_policy()

    registry.register(
        policy,
    )

    assert registry.get(
        policy.id,
    ) == policy


def test_registry_returns_none_for_unknown_policy() -> None:
    registry = FinancePolicyRegistry()

    assert registry.get(
        "finance.policy.unknown",
    ) is None


def test_registry_lists_registered_policies() -> None:
    registry = FinancePolicyRegistry()

    first = create_policy(
        "finance.policy.first",
    )
    second = create_policy(
        "finance.policy.second",
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


def test_registry_replaces_policy_with_same_identifier() -> None:
    registry = FinancePolicyRegistry()

    first = create_policy()

    second = FinancePolicy(
        id="finance.policy.basic",
        name="Updated Finance Policy",
        version="2.0.0",
        description="Updated requirements.",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.get(
        "finance.policy.basic",
    ) == second
