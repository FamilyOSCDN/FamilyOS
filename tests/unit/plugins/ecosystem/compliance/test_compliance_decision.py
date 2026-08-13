"""Tests for compliance decision derivation."""

from familyos_cli.plugins.ecosystem.compliance.compliance_decision import (
    ComplianceDecisionEvaluator,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
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

_PROFILE = ComplianceProfile(
    id="official",
    version="1.0.0",
    description="Test profile.",
    included_rule_ids=("PLUGIN-TEST-001",),
    blocking_severity_threshold=Severity.ERROR,
)


def _evaluation(
    outcome: RuleOutcome,
    *,
    severity: Severity = Severity.ERROR,
    mandatory: bool = False,
) -> RuleEvaluation:
    return RuleEvaluation(
        rule_id="PLUGIN-TEST-001",
        domain=ComplianceDomain.IDENTITY,
        outcome=outcome,
        severity=severity,
        validator_status=ValidatorStatus.SUCCESS,
        evidence_refs=(),
        message="",
        mandatory=mandatory,
    )


def test_all_pass_yields_compliant() -> None:
    """All PASS outcomes yield COMPLIANT."""

    status = ComplianceDecisionEvaluator.decide(
        (_evaluation(RuleOutcome.PASS),),
        _PROFILE,
    )

    assert status is ComplianceStatus.COMPLIANT


def test_any_error_yields_error_regardless_of_other_outcomes() -> None:
    """ERROR outcome takes precedence over everything else."""

    status = ComplianceDecisionEvaluator.decide(
        (
            _evaluation(RuleOutcome.ERROR),
            _evaluation(RuleOutcome.FAIL, mandatory=True),
        ),
        _PROFILE,
    )

    assert status is ComplianceStatus.ERROR


def test_mandatory_fail_yields_non_compliant_below_threshold() -> None:
    """A mandatory FAIL blocks compliance even under the severity threshold."""

    status = ComplianceDecisionEvaluator.decide(
        (_evaluation(RuleOutcome.FAIL, severity=Severity.INFO, mandatory=True),),
        _PROFILE,
    )

    assert status is ComplianceStatus.NON_COMPLIANT


def test_fail_at_or_above_threshold_yields_non_compliant() -> None:
    """A non-mandatory FAIL at or above the severity threshold blocks."""

    status = ComplianceDecisionEvaluator.decide(
        (_evaluation(RuleOutcome.FAIL, severity=Severity.CRITICAL),),
        _PROFILE,
    )

    assert status is ComplianceStatus.NON_COMPLIANT


def test_fail_below_threshold_does_not_block() -> None:
    """A non-mandatory FAIL below the severity threshold does not block."""

    status = ComplianceDecisionEvaluator.decide(
        (_evaluation(RuleOutcome.FAIL, severity=Severity.WARNING),),
        _PROFILE,
    )

    assert status is ComplianceStatus.COMPLIANT


def test_not_evaluated_yields_incomplete_when_not_blocked() -> None:
    """NOT_EVALUATED yields INCOMPLETE when nothing else blocks."""

    status = ComplianceDecisionEvaluator.decide(
        (_evaluation(RuleOutcome.NOT_EVALUATED),),
        _PROFILE,
    )

    assert status is ComplianceStatus.INCOMPLETE


def test_non_compliant_takes_precedence_over_incomplete() -> None:
    """NON_COMPLIANT outranks INCOMPLETE when both conditions are present."""

    status = ComplianceDecisionEvaluator.decide(
        (
            _evaluation(RuleOutcome.FAIL, mandatory=True),
            _evaluation(RuleOutcome.NOT_EVALUATED),
        ),
        _PROFILE,
    )

    assert status is ComplianceStatus.NON_COMPLIANT
