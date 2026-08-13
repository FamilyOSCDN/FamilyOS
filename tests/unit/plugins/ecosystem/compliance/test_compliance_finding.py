"""Tests for the compliance finding model."""

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)
from familyos_cli.plugins.ecosystem.compliance.finding_status import (
    FindingStatus,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity


def test_compliance_finding_construction() -> None:
    """A ComplianceFinding stores every provided field."""

    finding = ComplianceFinding(
        id="eval-1:PLUGIN-TEST-001",
        evaluation_id="eval-1",
        rule_id="PLUGIN-TEST-001",
        domain=ComplianceDomain.IDENTITY,
        severity=Severity.ERROR,
        category=FindingCategory.VIOLATION,
        status=FindingStatus.OPEN,
        title="Title",
        message="Message",
        evidence_refs=("test.validator:0",),
        location="",
        remediation="Fix it",
    )

    assert finding.rule_id == "PLUGIN-TEST-001"
    assert finding.category is FindingCategory.VIOLATION
    assert finding.status is FindingStatus.OPEN
