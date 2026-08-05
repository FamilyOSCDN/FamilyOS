"""Tests for EducationPolicyRegistry."""

from familyos_cli.plugins.builtin.education.policies.education_policy import (
    EducationPolicy,
)
from familyos_cli.plugins.builtin.education.policies.education_policy_registry import (
    EducationPolicyRegistry,
)


def create_policy(
    policy_id: str = "education.policy.basic",
) -> EducationPolicy:
    """Create test policy."""

    return EducationPolicy(
        id=policy_id,
        name="Basic Education Policy",
        level="basic",
    )


def test_registry_registers_policy() -> None:
    registry = EducationPolicyRegistry()

    policy = create_policy()

    registry.register(
        policy,
    )

    assert registry.get(
        policy.id,
    ) == policy


def test_registry_returns_none_for_unknown_policy() -> None:
    registry = EducationPolicyRegistry()

    assert registry.get(
        "education.policy.unknown",
    ) is None


def test_registry_lists_policies() -> None:
    registry = EducationPolicyRegistry()

    first = create_policy(
        "education.policy.first",
    )
    second = create_policy(
        "education.policy.second",
    )

    registry.register(first)
    registry.register(second)

    assert registry.list() == (
        first,
        second,
    )
