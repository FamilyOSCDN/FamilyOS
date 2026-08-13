"""Rule evaluation outcome model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.severity import Severity
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)


@dataclass(frozen=True, slots=True)
class RuleEvaluation:
    """Represent the result of evaluating one compliance rule."""

    rule_id: str
    domain: ComplianceDomain
    outcome: RuleOutcome
    severity: Severity
    validator_status: ValidatorStatus
    evidence_refs: tuple[str, ...]
    message: str
    mandatory: bool
