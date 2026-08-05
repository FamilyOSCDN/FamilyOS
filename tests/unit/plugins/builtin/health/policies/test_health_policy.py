"""Tests for HealthPolicy."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.health.policies.health_policy import (
    HealthPolicy,
)


def test_health_policy_can_be_created() -> None:
    """Health policy stores values."""

    policy = HealthPolicy(
        id="health.policy.wellness",
        name="Wellness Policy",
        version="1.0.0",
        description="Promotes healthy habits.",
    )

    assert policy.id == "health.policy.wellness"
    assert policy.name == "Wellness Policy"
    assert policy.version == "1.0.0"
    assert policy.description == (
        "Promotes healthy habits."
    )


def test_health_policy_description_is_optional() -> None:
    """Description defaults to empty."""

    policy = HealthPolicy(
        id="health.policy.basic",
        name="Basic Health Policy",
        version="1.0.0",
    )

    assert policy.description == ""


def test_health_policy_is_immutable() -> None:
    """Health policies cannot be modified."""

    policy = HealthPolicy(
        id="health.policy.basic",
        name="Basic Health Policy",
        version="1.0.0",
    )

    with pytest.raises(FrozenInstanceError):
        policy.version = "2.0.0"  # type: ignore[misc]
