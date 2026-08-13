"""Compliance finding generation."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)
from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)
from familyos_cli.plugins.ecosystem.compliance.finding_status import (
    FindingStatus,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome

_OUTCOME_TO_CATEGORY: dict[RuleOutcome, FindingCategory] = {
    RuleOutcome.FAIL: FindingCategory.VIOLATION,
    RuleOutcome.NOT_EVALUATED: FindingCategory.INCOMPLETE,
    RuleOutcome.ERROR: FindingCategory.VALIDATION_ERROR,
}


class FindingGenerator:
    """Derive compliance findings from rule evaluations.

    Findings are generated only for FAIL, NOT_EVALUATED, and ERROR
    outcomes; PASS and NOT_APPLICABLE never produce a finding.
    """

    @staticmethod
    def from_evaluation(
        rule: ComplianceRule,
        evaluation: RuleEvaluation,
        *,
        evaluation_id: str,
        finding_id: str,
    ) -> ComplianceFinding | None:
        """Build a finding for a rule evaluation, or None if none applies."""

        category = _OUTCOME_TO_CATEGORY.get(evaluation.outcome)

        if category is None:
            return None

        return ComplianceFinding(
            id=finding_id,
            evaluation_id=evaluation_id,
            rule_id=rule.id,
            domain=rule.domain,
            severity=rule.severity,
            category=category,
            status=FindingStatus.OPEN,
            title=rule.title,
            message=evaluation.message or rule.requirement,
            evidence_refs=evaluation.evidence_refs,
            location="",
            remediation=rule.remediation,
        )
