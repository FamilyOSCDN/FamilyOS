"""Official compliance profile."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_profile import (
    ComplianceProfile,
)
from familyos_cli.plugins.ecosystem.compliance.rules.default_rule_catalog import (
    DEFAULT_COMPLIANCE_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.severity import Severity

OFFICIAL_PROFILE = ComplianceProfile(
    id="official",
    version="1.0.0",
    description=(
        "Baseline compliance profile for FamilyOS official plugins, "
        "covering identity, metadata, structure, architecture, "
        "capabilities, and dependencies."
    ),
    included_rule_ids=tuple(
        rule.id for rule in DEFAULT_COMPLIANCE_RULES if "official" in rule.profiles
    ),
    excluded_rule_ids=(),
    mandatory_rule_ids=("PLUGIN-IDENT-003",),
    blocking_severity_threshold=Severity.ERROR,
)
