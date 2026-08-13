"""Compliance rule model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)
from familyos_cli.plugins.ecosystem.compliance.rule_lifecycle import (
    RuleLifecycle,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity


@dataclass(frozen=True, slots=True)
class ComplianceRule:
    """Represent one governed plugin compliance requirement.

    See docs/epics/EPIC-PLUGIN-002-plugin-compliance-framework/
    06-Compliance-Rule-Model.md for the full conceptual model.
    """

    id: str
    domain: ComplianceDomain
    title: str
    description: str
    requirement: str
    rationale: str
    severity: Severity
    applicability: RuleApplicability
    validator_id: str
    evidence_requirements: tuple[EvidenceType, ...]
    remediation: str
    lifecycle: RuleLifecycle = RuleLifecycle.ACTIVE
    mandatory: bool = False
    profiles: tuple[str, ...] = ()
