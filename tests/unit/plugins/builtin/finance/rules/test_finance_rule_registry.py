"""Tests for FinanceRuleRegistry."""

from familyos_cli.plugins.builtin.finance.rules.finance_rule import (
    FinanceRule,
)
from familyos_cli.plugins.builtin.finance.rules.finance_rule_registry import (
    FinanceRuleRegistry,
)


def create_rule(
    rule_id: str = "finance.rule.basic",
) -> FinanceRule:
    """Create a test finance rule."""

    return FinanceRule(
        id=rule_id,
        name="Basic Finance Rule",
        version="1.0.0",
        severity="LOW",
        description="Basic finance validation rule.",
    )


def test_registry_registers_rule() -> None:
    registry = FinanceRuleRegistry()

    rule = create_rule()

    registry.register(
        rule,
    )

    assert registry.get(
        rule.id,
    ) == rule


def test_registry_returns_none_for_unknown_rule() -> None:
    registry = FinanceRuleRegistry()

    assert registry.get(
        "finance.rule.unknown",
    ) is None


def test_registry_lists_registered_rules() -> None:
    registry = FinanceRuleRegistry()

    first = create_rule(
        "finance.rule.first",
    )
    second = create_rule(
        "finance.rule.second",
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


def test_registry_replaces_rule_with_same_identifier() -> None:
    registry = FinanceRuleRegistry()

    first = create_rule()

    second = FinanceRule(
        id="finance.rule.basic",
        name="Updated Finance Rule",
        version="2.0.0",
        severity="HIGH",
        description="Updated validation rule.",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    assert registry.get(
        "finance.rule.basic",
    ) == second
