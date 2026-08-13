"""Tests for dependencies domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.dependency_rules import (
    DEPENDENCY_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_dependency_rules_are_consistent() -> None:
    """Dependency rules satisfy the catalog consistency requirements."""

    assert len(DEPENDENCY_RULES) == 2
    assert_rule_catalog_is_consistent(DEPENDENCY_RULES)
