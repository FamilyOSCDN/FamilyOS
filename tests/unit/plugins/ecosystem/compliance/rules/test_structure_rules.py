"""Tests for structure domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.structure_rules import (
    STRUCTURE_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_structure_rules_are_consistent() -> None:
    """Structure rules satisfy the catalog consistency requirements."""

    assert len(STRUCTURE_RULES) == 3
    assert_rule_catalog_is_consistent(STRUCTURE_RULES)
