"""Identity domain compliance rules."""

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
from familyos_cli.plugins.ecosystem.compliance.plugin_classification import (
    PluginClassification,
)
from familyos_cli.plugins.ecosystem.compliance.rule_applicability import (
    RuleApplicability,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity

IDENTITY_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-IDENT-001",
        domain=ComplianceDomain.IDENTITY,
        title="Plugin manifest must exist and parse",
        description=(
            "Every plugin MUST provide a 'plugin.yaml' manifest at its "
            "package root, and that manifest MUST parse as a YAML mapping."
        ),
        requirement=(
            "A plugin.yaml file MUST exist at the plugin package root "
            "and MUST parse as a YAML mapping."
        ),
        rationale=(
            "The manifest is the sole authoritative source of plugin "
            "identity and discovery metadata; without it, no other "
            "compliance rule can be evaluated."
        ),
        severity=Severity.CRITICAL,
        applicability=RuleApplicability(),
        validator_id="identity.manifest-presence",
        evidence_requirements=(EvidenceType.STRUCTURE, EvidenceType.IDENTITY),
        remediation=(
            "Add a plugin.yaml file at the plugin package root containing "
            "at minimum id, name, version, author, description, module, "
            "class."
        ),
        mandatory=True,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-IDENT-002",
        domain=ComplianceDomain.IDENTITY,
        title="Plugin id must be a canonical Plugin Identifier",
        description=(
            "The manifest 'id' field MUST match the canonical FamilyOS "
            "Plugin Identifier pattern."
        ),
        requirement=(
            "Manifest 'id' MUST be present and MUST be a valid canonical "
            "Plugin Identifier."
        ),
        rationale=(
            "A stable, canonical identifier is required for plugin "
            "discovery, registration, and cross-referencing throughout "
            "the ecosystem."
        ),
        severity=Severity.CRITICAL,
        applicability=RuleApplicability(),
        validator_id="identity.id-format",
        evidence_requirements=(EvidenceType.IDENTITY,),
        remediation=(
            "Set manifest 'id' to a value matching "
            "'^[a-z][a-z0-9_]*(?:\\.[a-z][a-z0-9_]*)+$', e.g. "
            "'familyos.my_plugin'."
        ),
        mandatory=True,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-IDENT-003",
        domain=ComplianceDomain.IDENTITY,
        title="Official plugins must use the reserved namespace",
        description=(
            "Under the official profile, the manifest 'id' MUST start "
            "with the 'familyos.' namespace prefix."
        ),
        requirement=(
            "For official plugins, manifest 'id' MUST start with "
            "'familyos.'."
        ),
        rationale=(
            "Reserving the 'familyos.' namespace for official plugins "
            "prevents identifier collisions with third-party plugins."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(
            classifications=(PluginClassification.OFFICIAL,),
        ),
        validator_id="identity.namespace",
        evidence_requirements=(EvidenceType.IDENTITY,),
        remediation="Rename the plugin id to start with 'familyos.'.",
        mandatory=False,
        profiles=("official",),
    ),
)
