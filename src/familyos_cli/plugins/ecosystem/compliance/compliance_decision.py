"""Compliance decision derivation."""

from __future__ import annotations

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

_SEVERITY_ORDER: dict[Severity, int] = {
    Severity.INFO: 0,
    Severity.WARNING: 1,
    Severity.ERROR: 2,
    Severity.CRITICAL: 3,
}


class ComplianceDecisionEvaluator:
    """Derive the overall ComplianceStatus from rule evaluations and policy.

    Precedence: ERROR > NON_COMPLIANT > INCOMPLETE > COMPLIANT. A mandatory
    rule FAIL always forces NON_COMPLIANT regardless of severity policy.
    """

    @staticmethod
    def decide(
        evaluations: tuple[RuleEvaluation, ...],
        profile: ComplianceProfile,
    ) -> ComplianceStatus:
        """Derive the overall compliance status for one evaluation."""

        if any(
            evaluation.outcome is RuleOutcome.ERROR for evaluation in evaluations
        ):
            return ComplianceStatus.ERROR

        mandatory_blocked = any(
            evaluation.mandatory and evaluation.outcome is RuleOutcome.FAIL
            for evaluation in evaluations
        )

        threshold_rank = _SEVERITY_ORDER[profile.blocking_severity_threshold]

        severity_blocked = any(
            evaluation.outcome is RuleOutcome.FAIL
            and _SEVERITY_ORDER[evaluation.severity] >= threshold_rank
            for evaluation in evaluations
        )

        if mandatory_blocked or severity_blocked:
            return ComplianceStatus.NON_COMPLIANT

        incomplete = any(
            evaluation.outcome is RuleOutcome.NOT_EVALUATED
            for evaluation in evaluations
        )

        if incomplete:
            return ComplianceStatus.INCOMPLETE

        return ComplianceStatus.COMPLIANT
