"""Tests for the compliance rule registry."""

import pytest

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)
from familyos_cli.plugins.ecosystem.compliance.rule_registry import RuleRegistry
from familyos_cli.plugins.ecosystem.compliance.severity import Severity


def _make_rule(rule_id: str = "PLUGIN-TEST-001") -> ComplianceRule:
    return ComplianceRule(
        id=rule_id,
        domain=ComplianceDomain.IDENTITY,
        title="Test rule",
        description="Test rule description.",
        requirement="MUST do something.",
        rationale="Because tests.",
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="test.validator",
        evidence_requirements=(EvidenceType.IDENTITY,),
        remediation="Do something.",
    )


def test_register_and_get_rule() -> None:
    """A registered rule can be retrieved by id."""

    registry = RuleRegistry()
    rule = _make_rule()

    registry.register(rule)

    assert registry.get(rule.id) is rule


def test_register_duplicate_rule_raises() -> None:
    """Registering the same rule id twice raises ValueError."""

    registry = RuleRegistry()
    registry.register(_make_rule())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(_make_rule())


def test_get_missing_rule_raises() -> None:
    """Retrieving an unregistered rule id raises ValueError."""

    registry = RuleRegistry()

    with pytest.raises(ValueError, match="not registered"):
        registry.get("PLUGIN-MISSING-001")


def test_list_returns_all_rules() -> None:
    """list() returns every registered rule."""

    registry = RuleRegistry()
    first = _make_rule("PLUGIN-TEST-001")
    second = _make_rule("PLUGIN-TEST-002")

    registry.register(first)
    registry.register(second)

    assert set(registry.list()) == {first, second}
