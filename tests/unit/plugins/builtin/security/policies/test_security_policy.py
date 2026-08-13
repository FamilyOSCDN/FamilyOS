"""Tests for SecurityPolicy."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.security.policies.security_policy import (
    SecurityPolicy,
)


def create_policy(
    **overrides: str,
) -> SecurityPolicy:
    """Create a security policy for tests."""

    values = {
        "id": "security.policy.basic",
        "name": "Basic Security Policy",
        "version": "1.0.0",
        "description": "",
    }
    values.update(
        overrides,
    )

    return SecurityPolicy(
        id=values["id"],
        name=values["name"],
        version=values["version"],
        description=values["description"],
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
    policy = create_policy()

    assert policy.description == ""


def test_security_policy_is_immutable() -> None:
    policy = create_policy()

    with pytest.raises(FrozenInstanceError):
        policy.version = "2.0.0"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("field", "message"),
    [
        (
            "id",
            "Security policy id cannot be empty.",
        ),
        (
            "name",
            "Security policy name cannot be empty.",
        ),
        (
            "version",
            "Security policy version cannot be empty.",
        ),
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "   ",
    ],
)
def test_security_policy_rejects_empty_required_fields(
    field: str,
    message: str,
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=message,
    ):
        create_policy(
            **{
                field: invalid_value,
            },
        )
