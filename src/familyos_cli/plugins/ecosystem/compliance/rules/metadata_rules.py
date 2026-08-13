"""Metadata domain compliance rules."""

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

METADATA_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-META-001",
        domain=ComplianceDomain.METADATA,
        title="Plugin name must be present",
        description="The manifest 'name' field MUST be a non-empty string.",
        requirement="Manifest 'name' MUST be a non-empty string.",
        rationale=(
            "A human-readable name is required for developer tooling, "
            "reporting, and documentation."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="metadata.name-present",
        evidence_requirements=(EvidenceType.METADATA,),
        remediation="Set a non-empty 'name' field in plugin.yaml.",
        mandatory=True,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-META-002",
        domain=ComplianceDomain.METADATA,
        title="Plugin version must be valid semantic version",
        description=(
            "The manifest 'version' field MUST be a valid semantic "
            "version string."
        ),
        requirement="Manifest 'version' MUST parse as a valid semver string.",
        rationale=(
            "Dependency resolution and compatibility checks rely on "
            "well-formed semantic versions."
        ),
        severity=Severity.CRITICAL,
        applicability=RuleApplicability(),
        validator_id="metadata.version-format",
        evidence_requirements=(EvidenceType.METADATA,),
        remediation=(
            "Set 'version' to a valid semantic version, e.g. '1.0.0'."
        ),
        mandatory=True,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-META-003",
        domain=ComplianceDomain.METADATA,
        title="Plugin description should be meaningful",
        description=(
            "The manifest 'description' field SHOULD be present and "
            "provide enough detail to be useful (at least 20 characters)."
        ),
        requirement=(
            "Manifest 'description' SHOULD be present and at least 20 "
            "characters long."
        ),
        rationale=(
            "Short or missing descriptions provide little value to "
            "developers browsing the plugin ecosystem."
        ),
        severity=Severity.WARNING,
        applicability=RuleApplicability(),
        validator_id="metadata.description-quality",
        evidence_requirements=(EvidenceType.METADATA,),
        remediation=(
            "Expand the 'description' field to clearly explain the "
            "plugin's purpose."
        ),
        mandatory=False,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-META-004",
        domain=ComplianceDomain.METADATA,
        title="Manifest version must match runtime metadata version",
        description=(
            "The manifest 'version' MUST equal the 'version' declared on "
            "the loaded plugin class's PluginMetadata."
        ),
        requirement=(
            "Manifest 'version' MUST equal the loaded plugin's "
            "PluginMetadata.version."
        ),
        rationale=(
            "A mismatch between declared and implemented metadata "
            "indicates the manifest is stale or the plugin was not "
            "released correctly."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="metadata.consistency",
        evidence_requirements=(EvidenceType.METADATA,),
        remediation=(
            "Update plugin.yaml 'version' or the plugin class metadata "
            "so both declare the same version."
        ),
        mandatory=True,
        profiles=("official",),
    ),
)
