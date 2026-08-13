"""Tests for the rule evaluation model."""

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


def test_rule_evaluation_construction() -> None:
    """A RuleEvaluation stores every provided field."""

    evaluation = RuleEvaluation(
        rule_id="PLUGIN-TEST-001",
        domain=ComplianceDomain.IDENTITY,
        outcome=RuleOutcome.PASS,
        severity=Severity.ERROR,
        validator_status=ValidatorStatus.SUCCESS,
        evidence_refs=("test.validator:0",),
        message="",
        mandatory=True,
    )

    assert evaluation.outcome is RuleOutcome.PASS
    assert evaluation.mandatory is True
