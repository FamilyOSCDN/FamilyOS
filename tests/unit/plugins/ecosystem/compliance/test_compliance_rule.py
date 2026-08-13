"""Tests for the compliance rule model."""

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
from familyos_cli.plugins.ecosystem.compliance.rule_lifecycle import (
    RuleLifecycle,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity


def test_compliance_rule_defaults() -> None:
    """A ComplianceRule defaults to ACTIVE lifecycle and non-mandatory."""

    rule = ComplianceRule(
        id="PLUGIN-TEST-001",
        domain=ComplianceDomain.IDENTITY,
        title="Title",
        description="Description",
        requirement="MUST",
        rationale="Rationale",
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="test.validator",
        evidence_requirements=(EvidenceType.IDENTITY,),
        remediation="Fix it",
    )

    assert rule.lifecycle is RuleLifecycle.ACTIVE
    assert rule.mandatory is False
    assert rule.profiles == ()
