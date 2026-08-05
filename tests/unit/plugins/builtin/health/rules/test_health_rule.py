"""Tests for HealthRule."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.health.rules.health_rule import (
    HealthRule,
)


def test_health_rule_can_be_created() -> None:
    """Health rule stores values."""

    rule = HealthRule(
        id="health.rule.activity",
        name="Activity Rule",
        version="1.0.0",
        severity="HIGH",
        description="Checks activity requirements.",
    )

    assert rule.id == "health.rule.activity"
    assert rule.name == "Activity Rule"
    assert rule.version == "1.0.0"
    assert rule.severity == "HIGH"
    assert rule.description == (
        "Checks activity requirements."
    )


def test_health_rule_description_is_optional() -> None:
    """Description defaults to empty."""

    rule = HealthRule(
        id="health.rule.basic",
        name="Basic Health Rule",
        version="1.0.0",
        severity="LOW",
    )

    assert rule.description == ""


def test_health_rule_is_immutable() -> None:
    """Health rules cannot be modified."""

    rule = HealthRule(
        id="health.rule.basic",
        name="Basic Health Rule",
        version="1.0.0",
        severity="LOW",
    )

    with pytest.raises(FrozenInstanceError):
        rule.severity = "HIGH"  # type: ignore[misc]
