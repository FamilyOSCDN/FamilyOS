"""Shared fixtures for compliance reporting tests."""

from __future__ import annotations

from datetime import UTC, datetime

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_result import (
    ComplianceResult,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)
from familyos_cli.plugins.ecosystem.compliance.finding_status import (
    FindingStatus,
)
from familyos_cli.plugins.ecosystem.compliance.reporting.compliance_report import (
    ComplianceReport,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


def build_sample_report(*, with_finding: bool) -> ComplianceReport:
    """Build a small ComplianceReport for renderer tests."""

    now = datetime.now(UTC)

    evaluation = RuleEvaluation(
        rule_id="PLUGIN-TEST-001",
        domain=ComplianceDomain.IDENTITY,
        outcome=RuleOutcome.FAIL if with_finding else RuleOutcome.PASS,
        severity=Severity.ERROR,
        validator_status=ValidatorStatus.SUCCESS,
        evidence_refs=("test.validator:0",),
        message="Test message.",
        mandatory=False,
    )

    findings: tuple[ComplianceFinding, ...] = ()

    if with_finding:
        findings = (
            ComplianceFinding(
                id="eval-1:PLUGIN-TEST-001",
                evaluation_id="eval-1",
                rule_id="PLUGIN-TEST-001",
                domain=ComplianceDomain.IDENTITY,
                severity=Severity.ERROR,
                category=FindingCategory.VIOLATION,
                status=FindingStatus.OPEN,
                title="Test finding",
                message="Test message.",
                evidence_refs=("test.validator:0",),
                location="",
                remediation="Fix it.",
            ),
        )

    result = ComplianceResult(
        evaluation_id="eval-1",
        plugin_id="familyos.test",
        plugin_version="1.0.0",
        profile_id="official",
        status=(
            ComplianceStatus.NON_COMPLIANT
            if with_finding
            else ComplianceStatus.COMPLIANT
        ),
        rule_evaluations=(evaluation,),
        findings=findings,
        evidence=(),
        started_at=now,
        completed_at=now,
    )

    return ComplianceReport(
        schema_version="1.0.0",
        framework_version="1.0.0",
        profile_version="1.0.0",
        result=result,
    )
