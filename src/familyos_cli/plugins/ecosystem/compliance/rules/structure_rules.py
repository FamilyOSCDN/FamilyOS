"""Structure domain compliance rules."""

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

STRUCTURE_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-STRUCT-001",
        domain=ComplianceDomain.STRUCTURE,
        title="Plugin entry point must be resolvable",
        description=(
            "The manifest 'module'/'class' MUST import successfully, and "
            "'class' MUST be a subclass of the base Plugin contract."
        ),
        requirement=(
            "Manifest 'module' MUST import and 'class' MUST resolve to a "
            "subclass of familyos_cli.plugins.plugin.Plugin."
        ),
        rationale=(
            "A plugin that cannot be loaded cannot be activated or "
            "further validated."
        ),
        severity=Severity.CRITICAL,
        applicability=RuleApplicability(),
        validator_id="structure.entry-point",
        evidence_requirements=(EvidenceType.STRUCTURE,),
        remediation=(
            "Fix the 'module'/'class' manifest fields so they reference "
            "an importable Plugin subclass."
        ),
        mandatory=True,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-STRUCT-002",
        domain=ComplianceDomain.STRUCTURE,
        title="Plugin must be a proper package with a root-level manifest",
        description=(
            "The plugin root MUST contain '__init__.py', and 'plugin.yaml' "
            "MUST sit directly at that root."
        ),
        requirement=(
            "Plugin root MUST have '__init__.py' and 'plugin.yaml' MUST "
            "be located directly at the plugin root."
        ),
        rationale=(
            "A predictable package layout is required for reliable "
            "discovery and import."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="structure.package-layout",
        evidence_requirements=(EvidenceType.STRUCTURE,),
        remediation=(
            "Add an '__init__.py' file to the plugin root and keep "
            "plugin.yaml directly inside it."
        ),
        mandatory=False,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-STRUCT-003",
        domain=ComplianceDomain.STRUCTURE,
        title="Declared contribution paths must exist",
        description=(
            "Every template contribution's 'template_directory' returned "
            "by the plugin MUST exist on disk."
        ),
        requirement=(
            "Every TemplateContribution.template_directory MUST resolve "
            "to an existing directory."
        ),
        rationale=(
            "A declared but missing contribution path silently breaks "
            "generation for consumers of the plugin."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="structure.contribution-paths",
        evidence_requirements=(EvidenceType.STRUCTURE,),
        remediation=(
            "Create the missing template directory or correct the "
            "declared path."
        ),
        mandatory=False,
        profiles=("official",),
    ),
)
