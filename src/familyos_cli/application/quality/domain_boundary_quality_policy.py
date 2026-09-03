"""Governed initial repository domain-boundary requirement and rule."""

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityRequirement,
    QualityRequirementId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
)

ARCHITECTURE_CHECK_ID = QualityCheckId("QLT-CHECK-ARCHITECTURE")
DOMAIN_SOURCE_ROOT = "src/familyos_cli/domain"
DOMAIN_FORBIDDEN_MODULES = (
    "familyos_cli.application",
    "familyos_cli.infrastructure",
    "familyos_cli.interfaces",
)
DOMAIN_BOUNDARY_REQUIREMENT = QualityRequirement(
    id=QualityRequirementId("QLT-REQ-ARC-010"),
    title="Domain source must remain independent of outer layers",
    description="Domain source must not statically import application, infrastructure, or interfaces.",
    domain=QualityDomain("QLT-DOM-ARC"),
    authority="docs/00-foundation/Engineering-Constitution.md (Articles I and IV); docs/00-foundation/CLI-Architecture.md",
    mandatory=True,
    applicability="Repository Python domain source under src/familyos_cli/domain",
    verification="Static AST import analysis using QLT-CHECK-ARCHITECTURE",
)
DOMAIN_BOUNDARY_RULE = QualityRule(
    id=QualityRuleId("QLT-RULE-ARC-010"),
    requirement_id=DOMAIN_BOUNDARY_REQUIREMENT.id,
    domain=DOMAIN_BOUNDARY_REQUIREMENT.domain,
    severity=QualitySeverity.HIGH,
    description=DOMAIN_BOUNDARY_REQUIREMENT.description,
    executor="architecture",
)
