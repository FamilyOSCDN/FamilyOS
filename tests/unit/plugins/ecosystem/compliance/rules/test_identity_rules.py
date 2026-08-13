"""Tests for identity domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.identity_rules import (
    IDENTITY_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_identity_rules_are_consistent() -> None:
    """Identity rules satisfy the catalog consistency requirements."""

    assert len(IDENTITY_RULES) == 3
    assert_rule_catalog_is_consistent(IDENTITY_RULES)
