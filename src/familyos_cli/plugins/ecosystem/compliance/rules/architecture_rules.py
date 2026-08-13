"""Architecture domain compliance rules."""

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

ARCHITECTURE_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-ARCH-001",
        domain=ComplianceDomain.ARCHITECTURE,
        title="Plugin domain code must not import interface/application layers",
        description=(
            "Python files under the plugin's 'domain/' subpackage, if "
            "present, MUST NOT import from familyos_cli.interfaces or "
            "familyos_cli.application."
        ),
        requirement=(
            "Files under <plugin>/domain/ MUST NOT import "
            "familyos_cli.interfaces or familyos_cli.application."
        ),
        rationale=(
            "Domain code depending on outer architectural layers "
            "inverts the dependency direction required by Clean "
            "Architecture."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="architecture.import-boundary",
        evidence_requirements=(EvidenceType.ARCHITECTURE,),
        remediation=(
            "Remove the offending import and depend on an abstraction "
            "instead, or move the logic to an appropriate outer layer."
        ),
        mandatory=False,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-ARCH-002",
        domain=ComplianceDomain.ARCHITECTURE,
        title="No wildcard imports",
        description=(
            "Python files in the plugin package tree MUST NOT use "
            "'from x import *' wildcard imports."
        ),
        requirement="Plugin source MUST NOT contain wildcard imports.",
        rationale=(
            "Wildcard imports obscure dependencies and increase the risk "
            "of name collisions."
        ),
        severity=Severity.WARNING,
        applicability=RuleApplicability(),
        validator_id="architecture.no-wildcard-imports",
        evidence_requirements=(EvidenceType.ARCHITECTURE,),
        remediation="Replace wildcard imports with explicit imports.",
        mandatory=False,
        profiles=("official",),
    ),
)
