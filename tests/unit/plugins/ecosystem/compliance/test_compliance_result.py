"""Tests for the compliance result model."""

from datetime import UTC, datetime

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_result import (
    ComplianceResult,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


def _evaluation(
    outcome: RuleOutcome,
    *,
    mandatory: bool,
) -> RuleEvaluation:
    return RuleEvaluation(
        rule_id="PLUGIN-TEST-001",
        domain=ComplianceDomain.IDENTITY,
        outcome=outcome,
        severity=Severity.ERROR,
        validator_status=ValidatorStatus.SUCCESS,
        evidence_refs=(),
        message="",
        mandatory=mandatory,
    )


def _result(evaluations: tuple[RuleEvaluation, ...], status: ComplianceStatus) -> ComplianceResult:
    now = datetime.now(UTC)

    return ComplianceResult(
        evaluation_id="eval-1",
        plugin_id="familyos.test",
        plugin_version="1.0.0",
        profile_id="official",
        status=status,
        rule_evaluations=evaluations,
        findings=(),
        evidence=(),
        started_at=now,
        completed_at=now,
    )


def test_is_compliant_true_for_compliant_status() -> None:
    """is_compliant() is True only for COMPLIANT status."""

    result = _result((), ComplianceStatus.COMPLIANT)

    assert result.is_compliant() is True


def test_is_compliant_false_for_non_compliant_status() -> None:
    """is_compliant() is False for NON_COMPLIANT status."""

    result = _result((), ComplianceStatus.NON_COMPLIANT)

    assert result.is_compliant() is False


def test_mandatory_failures_excludes_pass_and_not_applicable() -> None:
    """mandatory_failures() excludes PASS and NOT_APPLICABLE outcomes."""

    passing = _evaluation(RuleOutcome.PASS, mandatory=True)
    not_applicable = _evaluation(RuleOutcome.NOT_APPLICABLE, mandatory=True)
    failing = _evaluation(RuleOutcome.FAIL, mandatory=True)
    non_mandatory_failing = _evaluation(RuleOutcome.FAIL, mandatory=False)

    result = _result(
        (passing, not_applicable, failing, non_mandatory_failing),
        ComplianceStatus.NON_COMPLIANT,
    )

    assert result.mandatory_failures() == (failing,)
