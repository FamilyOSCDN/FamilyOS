"""Tests for metadata domain compliance rules."""

from familyos_cli.plugins.ecosystem.compliance.rules.metadata_rules import (
    METADATA_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_metadata_rules_are_consistent() -> None:
    """Metadata rules satisfy the catalog consistency requirements."""

    assert len(METADATA_RULES) == 4
    assert_rule_catalog_is_consistent(METADATA_RULES)
