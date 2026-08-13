"""Quality domain compliance rules."""

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

QUALITY_RULES: tuple[ComplianceRule, ...] = (
    ComplianceRule(
        id="PLUGIN-QLT-001",
        domain=ComplianceDomain.QUALITY,
        title="Plugin source must pass Ruff checks",
        description=(
            "Python files under the plugin's own source subtree MUST pass "
            "Ruff checks with zero violations."
        ),
        requirement="Plugin source MUST report zero Ruff violations.",
        rationale=(
            "Unaddressed Ruff violations indicate style, correctness, or "
            "import-hygiene defects in the plugin's own code."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="quality.ruff",
        evidence_requirements=(EvidenceType.QUALITY,),
        remediation="Resolve the reported Ruff violations in the plugin source.",
        mandatory=False,
        profiles=("official",),
    ),
    ComplianceRule(
        id="PLUGIN-QLT-002",
        domain=ComplianceDomain.QUALITY,
        title="Plugin source must pass MyPy checks",
        description=(
            "Python files under the plugin's own source subtree MUST pass "
            "MyPy checks with zero type errors."
        ),
        requirement="Plugin source MUST report zero MyPy type errors.",
        rationale=(
            "Unresolved type errors indicate the plugin's own code does "
            "not honor the type contracts it declares or depends on."
        ),
        severity=Severity.ERROR,
        applicability=RuleApplicability(),
        validator_id="quality.mypy",
        evidence_requirements=(EvidenceType.QUALITY,),
        remediation="Resolve the reported MyPy type errors in the plugin source.",
        mandatory=False,
        profiles=("official",),
    ),
)
