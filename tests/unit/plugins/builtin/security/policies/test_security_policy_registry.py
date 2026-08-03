from familyos_cli.plugins.builtin.security.policies.security_policy import (
    SecurityPolicy,
)
from familyos_cli.plugins.builtin.security.policies.security_policy_registry import (
    SecurityPolicyRegistry,
)


def create_policy(
    policy_id: str = "security.policy.basic",
) -> SecurityPolicy:
    """Create a test security policy."""

    return SecurityPolicy(
        id=policy_id,
        name="Basic Security Policy",
        version="1.0.0",
        description="Basic security requirements.",
    )


def test_registry_registers_policy() -> None:
    registry = SecurityPolicyRegistry()

    policy = create_policy()

    registry.register(
        policy,
    )

    assert registry.get(
        policy.id,
    ) == policy


def test_registry_returns_none_for_unknown_policy() -> None:
    registry = SecurityPolicyRegistry()

    assert registry.get(
        "security.policy.unknown",
    ) is None


def test_registry_lists_registered_policies() -> None:
    registry = SecurityPolicyRegistry()

    first = create_policy(
        "security.policy.first",
    )
    second = create_policy(
        "security.policy.second",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    policies = registry.list()

    assert policies == (
        first,
        second,
    )


def test_registry_replaces_policy_with_same_identifier() -> None:
    registry = SecurityPolicyRegistry()

    first = create_policy()

    second = SecurityPolicy(
        id="security.policy.basic",
        name="Updated Security Policy",
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
        "security.policy.basic",
    ) == second
