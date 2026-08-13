"""Compliance result model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.ecosystem.compliance.rule_evaluation import (
    RuleEvaluation,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome


@dataclass(frozen=True, slots=True)
class ComplianceResult:
    """Represent the complete, immutable outcome of a compliance evaluation."""

    evaluation_id: str
    plugin_id: str
    plugin_version: str
    profile_id: str
    status: ComplianceStatus
    rule_evaluations: tuple[RuleEvaluation, ...]
    findings: tuple[ComplianceFinding, ...]
    evidence: tuple[ComplianceEvidence, ...]
    started_at: datetime
    completed_at: datetime

    def is_compliant(self) -> bool:
        """Return whether the overall status is COMPLIANT."""

        return self.status is ComplianceStatus.COMPLIANT

    def mandatory_failures(self) -> tuple[RuleEvaluation, ...]:
        """Return mandatory rule evaluations that did not PASS or NOT_APPLICABLE."""

        return tuple(
            evaluation
            for evaluation in self.rule_evaluations
            if evaluation.mandatory
            and evaluation.outcome
            not in (RuleOutcome.PASS, RuleOutcome.NOT_APPLICABLE)
        )
