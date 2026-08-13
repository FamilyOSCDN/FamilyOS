"""Tests for capabilities domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.capability_rules import (
    CAPABILITY_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_capability_rules_are_consistent() -> None:
    """Capability rules satisfy the catalog consistency requirements."""

    assert len(CAPABILITY_RULES) == 2
    assert_rule_catalog_is_consistent(CAPABILITY_RULES)
