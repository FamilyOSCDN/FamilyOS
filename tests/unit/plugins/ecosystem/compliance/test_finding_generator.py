"""Tests for compliance finding generation."""

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
from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)
from familyos_cli.plugins.ecosystem.compliance.finding_generator import (
    FindingGenerator,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)

_RULE = ComplianceRule(
    id="PLUGIN-TEST-001",
    domain=ComplianceDomain.IDENTITY,
    title="Title",
    description="Description",
    requirement="MUST do something.",
    rationale="Rationale",
    severity=Severity.ERROR,
    applicability=RuleApplicability(),
    validator_id="test.validator",
    evidence_requirements=(EvidenceType.IDENTITY,),
    remediation="Fix it",
)


def _evaluation(outcome: RuleOutcome) -> RuleEvaluation:
    return RuleEvaluation(
        rule_id=_RULE.id,
        domain=_RULE.domain,
        outcome=outcome,
        severity=_RULE.severity,
        validator_status=ValidatorStatus.SUCCESS,
        evidence_refs=("test.validator:0",),
        message="",
        mandatory=False,
    )


@pytest.mark.parametrize(
    ("outcome", "expected_category"),
    [
        (RuleOutcome.FAIL, FindingCategory.VIOLATION),
        (RuleOutcome.NOT_EVALUATED, FindingCategory.INCOMPLETE),
        (RuleOutcome.ERROR, FindingCategory.VALIDATION_ERROR),
    ],
)
def test_from_evaluation_generates_finding_for_actionable_outcomes(
    outcome: RuleOutcome,
    expected_category: FindingCategory,
) -> None:
    """FAIL/NOT_EVALUATED/ERROR outcomes produce a categorized finding."""

    finding = FindingGenerator.from_evaluation(
        _RULE,
        _evaluation(outcome),
        evaluation_id="eval-1",
        finding_id="eval-1:PLUGIN-TEST-001",
    )

    assert finding is not None
    assert finding.category is expected_category
    assert finding.message == _RULE.requirement


@pytest.mark.parametrize("outcome", [RuleOutcome.PASS, RuleOutcome.NOT_APPLICABLE])
def test_from_evaluation_returns_none_for_non_actionable_outcomes(
    outcome: RuleOutcome,
) -> None:
    """PASS/NOT_APPLICABLE outcomes never produce a finding."""

    finding = FindingGenerator.from_evaluation(
        _RULE,
        _evaluation(outcome),
        evaluation_id="eval-1",
        finding_id="eval-1:PLUGIN-TEST-001",
    )

    assert finding is None
