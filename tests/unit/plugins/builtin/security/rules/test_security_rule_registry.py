import pytest

from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)
from familyos_cli.plugins.builtin.security.rules.security_rule_registry import (
    SecurityRuleRegistry,
)


def create_rule(
    rule_id: str = "security.rule.basic",
) -> SecurityRule:
    """Create a test security rule."""

    return SecurityRule(
        id=rule_id,
        name="Basic Security Rule",
        version="1.0.0",
        severity="LOW",
        description="Basic security validation rule.",
    )


def test_registry_registers_rule() -> None:
    registry = SecurityRuleRegistry()

    rule = create_rule()

    registry.register(
        rule,
    )

    assert registry.get(
        rule.id,
    ) == rule


def test_registry_returns_none_for_unknown_rule() -> None:
    registry = SecurityRuleRegistry()

    assert registry.get(
        "security.rule.unknown",
    ) is None


def test_registry_lists_registered_rules() -> None:
    registry = SecurityRuleRegistry()

    first = create_rule(
        "security.rule.first",
    )
    second = create_rule(
        "security.rule.second",
    )

    registry.register(
        first,
    )
    registry.register(
        second,
    )

    rules = registry.list()

    assert rules == (
        first,
        second,
    )


def test_registry_rejects_duplicate_rule() -> None:
    registry = SecurityRuleRegistry()

    first = create_rule()

    second = SecurityRule(
        id="security.rule.basic",
        name="Updated Security Rule",
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
        "security.rule.basic",
    ) == first
