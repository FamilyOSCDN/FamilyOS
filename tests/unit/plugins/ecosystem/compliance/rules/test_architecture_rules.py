"""Tests for architecture domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.architecture_rules import (
    ARCHITECTURE_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_architecture_rules_are_consistent() -> None:
    """Architecture rules satisfy the catalog consistency requirements."""

    assert len(ARCHITECTURE_RULES) == 2
    assert_rule_catalog_is_consistent(ARCHITECTURE_RULES)
