"""Tests for compliance rule lifecycle states."""

from familyos_cli.plugins.ecosystem.compliance.rule_lifecycle import (
    RuleLifecycle,
)


def test_rule_lifecycle_values() -> None:
    """Rule lifecycle states expose stable serialized values."""

    assert RuleLifecycle.DRAFT.value == "draft"
    assert RuleLifecycle.ACTIVE.value == "active"
    assert RuleLifecycle.DEPRECATED.value == "deprecated"
    assert RuleLifecycle.RETIRED.value == "retired"
