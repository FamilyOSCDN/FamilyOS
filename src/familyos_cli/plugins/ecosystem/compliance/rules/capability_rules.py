"""Capabilities domain compliance rules."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_domain import (
    ComplianceDomain,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)
from familyos_cli.plugins.ecosystem.compliance.evidence_type import (
    EvidenceType,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity

CAPABILITY_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-CAP-001",
        domain=ComplianceDomain.CAPABILITIES,
        title="Capability identifiers must be namespaced under the plugin id",
        description=(
            "Every capability id returned by the plugin MUST be a valid "
            "canonical capability identifier AND MUST be namespaced under "
            "the plugin's own manifest id."
        ),
        requirement=(
            "Every PluginCapability.id MUST be a valid PluginCapabilityId "
            "and MUST start with '<plugin manifest id>.'."
        ),
        rationale=(
            "Namespacing capability identifiers under the owning "
            "plugin's id prevents cross-plugin capability collisions."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="capabilities.namespace",
        evidence_requirements=(EvidenceType.CAPABILITY,),
        remediation=(
            "Rename capability identifiers to start with the plugin's "
            "own manifest id, e.g. 'familyos.my_plugin.my_capability'."
        ),
        mandatory=True,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-CAP-002",
        domain=ComplianceDomain.CAPABILITIES,
        title="Capability display names must be present and unique",
        description=(
            "Every capability's 'display_name' MUST be non-empty and "
            "unique within the plugin."
        ),
        requirement=(
            "Capability display_name values MUST be non-empty and "
            "unique within the plugin."
        ),
        rationale=(
            "Duplicate or empty display names create ambiguous developer "
            "tooling output."
        ),
        severity=Severity.WARNING,
        applicability=RuleApplicability(),
        validator_id="capabilities.uniqueness",
        evidence_requirements=(EvidenceType.CAPABILITY,),
        remediation=(
            "Give each capability a unique, non-empty display_name."
        ),
        mandatory=False,
        profiles=("official",),
    ),
)
