"""Compliance finding model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)
from familyos_cli.plugins.ecosystem.compliance.finding_status import (
    FindingStatus,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity


@dataclass(frozen=True, slots=True)
class ComplianceFinding:
    """Represent one occurrence of a compliance-relevant condition.

    A finding records what a specific evaluation observed; it does not by
    itself determine overall compliance (see
    :class:`~familyos_cli.plugins.ecosystem.compliance.compliance_decision.ComplianceDecisionEvaluator`).
    """

    id: str
    evaluation_id: str
    rule_id: str
    domain: ComplianceDomain
    severity: Severity
    category: FindingCategory
    status: FindingStatus
    title: str
    message: str
    evidence_refs: tuple[str, ...]
    location: str
    remediation: str
