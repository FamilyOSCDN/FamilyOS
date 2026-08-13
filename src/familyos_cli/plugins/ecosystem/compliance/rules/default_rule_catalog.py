"""Default compliance rule catalog."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)
from familyos_cli.plugins.ecosystem.compliance.rules.architecture_rules import (
    ARCHITECTURE_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.rules.capability_rules import (
    CAPABILITY_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.rules.dependency_rules import (
    DEPENDENCY_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.rules.identity_rules import (
    IDENTITY_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.rules.metadata_rules import (
    METADATA_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.rules.quality_rules import (
    QUALITY_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.rules.structure_rules import (
    STRUCTURE_RULES,
)

DEFAULT_COMPLIANCE_RULES: tuple[ComplianceRule, ...] = (
    *IDENTITY_RULES,
    *METADATA_RULES,
    *STRUCTURE_RULES,
    *ARCHITECTURE_RULES,
    *CAPABILITY_RULES,
    *DEPENDENCY_RULES,
    *QUALITY_RULES,
)
