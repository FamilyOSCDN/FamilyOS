from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.security.policies.security_policy import (
    SecurityPolicy,
)


def test_security_policy_can_be_created() -> None:
    policy = SecurityPolicy(
        id="security.policy.account-protection",
        name="Account Protection Policy",
        version="1.0.0",
        description="Protects user account access.",
    )

    assert policy.id == "security.policy.account-protection"
    assert policy.name == "Account Protection Policy"
    assert policy.version == "1.0.0"
    assert policy.description == (
        "Protects user account access."
    )


def test_security_policy_description_is_optional() -> None:
    policy = SecurityPolicy(
        id="security.policy.basic",
        name="Basic Security Policy",
        version="1.0.0",
    )

    assert policy.description == ""


def test_security_policy_is_immutable() -> None:
    policy = SecurityPolicy(
        id="security.policy.basic",
        name="Basic Security Policy",
        version="1.0.0",
    )

    with pytest.raises(FrozenInstanceError):
        policy.version = "2.0.0"  # type: ignore[misc]
