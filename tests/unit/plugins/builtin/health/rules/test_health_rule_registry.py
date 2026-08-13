"""Tests for HealthRuleRegistry."""

import pytest

from familyos_cli.plugins.builtin.health.rules.health_rule import (
    HealthRule,
)
from familyos_cli.plugins.builtin.health.rules.health_rule_registry import (
    HealthRuleRegistry,
)


def create_rule(
    rule_id: str = "health.rule.basic",
) -> HealthRule:
    """Create a test health rule."""

    return HealthRule(
        id=rule_id,
        name="Basic Health Rule",
        version="1.0.0",
        severity="LOW",
        description="Basic health validation rule.",
    )


def test_registry_registers_rule() -> None:
    registry = HealthRuleRegistry()

    rule = create_rule()

    registry.register(
        rule,
    )

    assert registry.get(
        rule.id,
    ) == rule


def test_registry_returns_none_for_unknown_rule() -> None:
    registry = HealthRuleRegistry()

    assert registry.get(
        "health.rule.unknown",
    ) is None


def test_registry_lists_registered_rules() -> None:
    registry = HealthRuleRegistry()

    first = create_rule(
        "health.rule.first",
    )
    second = create_rule(
        "health.rule.second",
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


def test_registry_rejects_duplicate_rule() -> None:
    registry = HealthRuleRegistry()

    first = create_rule()

    second = HealthRule(
        id="health.rule.basic",
        name="Updated Health Rule",
        version="2.0.0",
        severity="HIGH",
        description="Updated validation rule.",
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
        "health.rule.basic",
    ) == first
