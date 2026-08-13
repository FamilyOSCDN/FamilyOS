"""Tests for EducationRuleRegistry."""

import pytest

from familyos_cli.plugins.builtin.education.rules.education_rule import (
    EducationRule,
)
from familyos_cli.plugins.builtin.education.rules.education_rule_registry import (
    EducationRuleRegistry,
)


def create_rule(
    rule_id: str = "education.rule.basic",
) -> EducationRule:
    """Create test rule."""

    return EducationRule(
        id=rule_id,
        name="Basic Learning Rule",
        level="basic",
    )


def test_registry_registers_rule() -> None:
    """Registered rules should be retrievable."""

    registry = EducationRuleRegistry()

    rule = create_rule()

    registry.register(
        rule,
    )

    assert registry.get(
        rule.id,
    ) == rule


def test_registry_returns_none_for_unknown_rule() -> None:
    """Unknown rule identifiers should return none."""

    registry = EducationRuleRegistry()

    assert registry.get(
        "education.rule.unknown",
    ) is None


def test_registry_lists_rules() -> None:
    """Rules should be listed in registration order."""

    registry = EducationRuleRegistry()

    first = create_rule(
        "education.rule.first",
    )
    second = create_rule(
        "education.rule.second",
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


def test_registry_rejects_duplicate_rule_id() -> None:
    """Duplicate rule identifiers should be rejected."""

    registry = EducationRuleRegistry()

    first = create_rule()
    duplicate = EducationRule(
        id=first.id,
        name="Replacement Rule",
        level="critical",
    )

    registry.register(
        first,
    )

    with pytest.raises(
        ValueError,
        match=(
            "Education rule "
            "'education.rule.basic' "
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
