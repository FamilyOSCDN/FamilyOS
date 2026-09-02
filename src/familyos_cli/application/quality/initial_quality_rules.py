"""Governed Phase 12 rules for the initial execution-binding surface."""
from familyos_cli.domain.quality import (
    QualityDomain,
    QualityRequirementId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
)

STATIC_ANALYSIS_RULE = QualityRule(QualityRuleId("QLT-RULE-STA-001"), None, QualityDomain("QLT-DOM-MNT"), QualitySeverity.MEDIUM, "Python source must satisfy configured static analysis requirements.", "ruff")
TYPE_VERIFICATION_RULE = QualityRule(QualityRuleId("QLT-RULE-TYP-001"), QualityRequirementId("QLT-REQ-TYP-001"), QualityDomain("QLT-DOM-COR"), QualitySeverity.HIGH, "Public Python interfaces must satisfy configured type verification requirements.", "mypy")
REQUIRED_TESTS_RULE = QualityRule(QualityRuleId("QLT-RULE-TST-001"), None, QualityDomain("QLT-DOM-TST"), QualitySeverity.CRITICAL, "Required tests selected for the active quality profile must pass.", "pytest")
DOCUMENTATION_RULE = QualityRule(QualityRuleId("QLT-RULE-DOC-001"), None, QualityDomain("QLT-DOM-DOC"), QualitySeverity.HIGH, "Required canonical documentation must satisfy configured documentation validation requirements.", "documentation")
PLUGIN_COMPLIANCE_INTEGRATION_RULE = QualityRule(QualityRuleId("QLT-RULE-CPL-001"), None, QualityDomain("QLT-DOM-CPL"), QualitySeverity.HIGH, "Authoritative plugin compliance evaluation must complete successfully for an applicable plugin target.", "plugin_compliance")
INITIAL_QUALITY_RULES = (STATIC_ANALYSIS_RULE, TYPE_VERIFICATION_RULE, REQUIRED_TESTS_RULE, DOCUMENTATION_RULE, PLUGIN_COMPLIANCE_INTEGRATION_RULE)
