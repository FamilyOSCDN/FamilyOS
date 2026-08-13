"""Tests for the aggregated default compliance rule catalog."""

from familyos_cli.plugins.ecosystem.compliance.rules.default_rule_catalog import (
    DEFAULT_COMPLIANCE_RULES,
)
from tests.unit.plugins.ecosystem.compliance.rules.rule_catalog_assertions import (
    assert_rule_catalog_is_consistent,
)


def test_default_rule_catalog_has_eighteen_rules() -> None:
    """The default catalog matches the planned initial slice size."""

    assert len(DEFAULT_COMPLIANCE_RULES) == 18


def test_default_rule_catalog_is_consistent() -> None:
    """The aggregated catalog satisfies the catalog consistency requirements."""

    assert_rule_catalog_is_consistent(DEFAULT_COMPLIANCE_RULES)
