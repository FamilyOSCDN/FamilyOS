"""Dependencies domain compliance rules."""

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

DEPENDENCY_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-DEP-001",
        domain=ComplianceDomain.DEPENDENCIES,
        title="Declared dependency expressions must be well-formed",
        description=(
            "If the manifest declares a 'dependencies' list, every entry "
            "MUST parse as a valid plugin dependency expression (a "
            "canonical plugin id with an optional version constraint)."
        ),
        requirement=(
            "Every declared dependency entry MUST parse as "
            "'<PluginId>[<constraint>]'."
        ),
        rationale=(
            "Malformed dependency expressions cannot be resolved by the "
            "plugin resolution pipeline."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="dependencies.expression-format",
        evidence_requirements=(EvidenceType.DEPENDENCY,),
        remediation=(
            "Correct the dependency entry to '<plugin id>[<version "
            "constraint>]', e.g. 'familyos.documentation>=1.0.0'."
        ),
        mandatory=False,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-DEP-002",
        domain=ComplianceDomain.DEPENDENCIES,
        title="Plugin must not declare a dependency on itself",
        description=(
            "None of the declared dependency plugin ids MAY equal the "
            "plugin's own manifest id."
        ),
        requirement="No declared dependency plugin id MAY equal the plugin's own id.",
        rationale=(
            "A self-dependency cannot be satisfied and indicates a "
            "manifest authoring error."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="dependencies.no-self-dependency",
        evidence_requirements=(EvidenceType.DEPENDENCY,),
        remediation="Remove the self-referencing dependency entry.",
        mandatory=False,
        profiles=("official",),
    ),
)
