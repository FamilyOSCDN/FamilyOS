"""Tests for quality domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.quality_rules import (
    QUALITY_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_quality_rules_are_consistent() -> None:
    """Quality rules satisfy the catalog consistency requirements."""

    assert len(QUALITY_RULES) == 2
    assert_rule_catalog_is_consistent(QUALITY_RULES)


def test_quality_rule_ids_are_stable() -> None:
    """Quality rule identifiers and validator bindings remain stable."""

    rules_by_id = {rule.id: rule for rule in QUALITY_RULES}

    assert rules_by_id["PLUGIN-QLT-001"].validator_id == "quality.ruff"
    assert rules_by_id["PLUGIN-QLT-002"].validator_id == "quality.mypy"

    for rule in QUALITY_RULES:
        assert "official" in rule.profiles
