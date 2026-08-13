"""Tests for EducationPolicyRegistry."""

import pytest

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
    """Registered policies should be retrievable."""

    registry = EducationPolicyRegistry()

    policy = create_policy()

    registry.register(
        policy,
    )

    assert registry.get(
        policy.id,
    ) == policy


def test_registry_returns_none_for_unknown_policy() -> None:
    """Unknown policy identifiers should return none."""

    registry = EducationPolicyRegistry()

    assert registry.get(
        "education.policy.unknown",
    ) is None


def test_registry_lists_policies() -> None:
    """Policies should be listed in registration order."""

    registry = EducationPolicyRegistry()

    first = create_policy(
        "education.policy.first",
    )
    second = create_policy(
        "education.policy.second",
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


def test_registry_rejects_duplicate_policy_id() -> None:
    """Duplicate policy identifiers should be rejected."""

    registry = EducationPolicyRegistry()

    first = create_policy()
    duplicate = EducationPolicy(
        id=first.id,
        name="Replacement Policy",
        level="critical",
    )

    registry.register(
        first,
    )

    with pytest.raises(
        ValueError,
        match=(
            "Education policy "
            "'education.policy.basic' "
            "is already registered."
        ),
    ):
        registry.register(
            duplicate,
        )

    assert registry.get(
        first.id,
    ) == first

    assert registry.list() == (
        first,
    )
