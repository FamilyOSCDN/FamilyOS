"""Tests for CommunicationPolicy."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.communication.policies import (
    CommunicationPolicy,
)


def test_communication_policy_can_be_created() -> None:
    policy = CommunicationPolicy(
        id="communication.policy.retention",
        name="Communication Retention Policy",
        version="1.0.0",
        description=(
            "Defines communication retention rules."
        ),
    )

    assert policy.id == (
        "communication.policy.retention"
    )

    assert policy.name == (
        "Communication Retention Policy"
    )

    assert policy.version == "1.0.0"

    assert policy.description == (
        "Defines communication retention rules."
    )


def test_communication_policy_description_is_optional() -> None:
    policy = CommunicationPolicy(
        id="communication.policy.basic",
        name="Basic Communication Policy",
        version="1.0.0",
    )

    assert policy.description == ""


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("id", ""),
        ("name", ""),
        ("version", ""),
        ("id", "   "),
        ("name", "   "),
        ("version", "   "),
    ],
)
def test_communication_policy_rejects_empty_required_fields(
    field_name: str,
    field_value: str,
) -> None:
    values = {
        "id": "communication.policy.basic",
        "name": "Basic Communication Policy",
        "version": "1.0.0",
    }

    values[field_name] = field_value

    with pytest.raises(ValueError):
        CommunicationPolicy(**values)


def test_communication_policy_is_immutable() -> None:
    policy = CommunicationPolicy(
        id="communication.policy.basic",
        name="Basic Communication Policy",
        version="1.0.0",
    )

    with pytest.raises(FrozenInstanceError):
        policy.version = "2.0.0"  # type: ignore[misc]
