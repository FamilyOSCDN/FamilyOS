from familyos_cli.application.quality.initial_quality_rules import (
    DOCUMENTATION_RULE,
    INITIAL_QUALITY_RULES,
    PLUGIN_COMPLIANCE_INTEGRATION_RULE,
    REQUIRED_TESTS_RULE,
    STATIC_ANALYSIS_RULE,
    TYPE_VERIFICATION_RULE,
)
from familyos_cli.domain.quality import QualitySeverity


def test_initial_rule_set_is_exact_and_deterministic() -> None:
    assert tuple(str(rule.id) for rule in INITIAL_QUALITY_RULES) == ("QLT-RULE-STA-001", "QLT-RULE-TYP-001", "QLT-RULE-TST-001", "QLT-RULE-DOC-001", "QLT-RULE-CPL-001")

def test_initial_rules_match_frozen_contract() -> None:
    actual = tuple((str(r.id), None if r.requirement_id is None else str(r.requirement_id), str(r.domain), r.severity, r.executor) for r in INITIAL_QUALITY_RULES)
    assert actual == (("QLT-RULE-STA-001", None, "QLT-DOM-MNT", QualitySeverity.MEDIUM, "ruff"), ("QLT-RULE-TYP-001", "QLT-REQ-TYP-001", "QLT-DOM-COR", QualitySeverity.HIGH, "mypy"), ("QLT-RULE-TST-001", None, "QLT-DOM-TST", QualitySeverity.CRITICAL, "pytest"), ("QLT-RULE-DOC-001", None, "QLT-DOM-DOC", QualitySeverity.HIGH, "documentation"), ("QLT-RULE-CPL-001", None, "QLT-DOM-CPL", QualitySeverity.HIGH, "plugin_compliance"))
    assert STATIC_ANALYSIS_RULE.description.startswith("Python source")
    assert TYPE_VERIFICATION_RULE.description.startswith("Public Python interfaces")
    assert REQUIRED_TESTS_RULE.description.startswith("Required tests")
    assert DOCUMENTATION_RULE.description.startswith("Required canonical documentation")
    assert PLUGIN_COMPLIANCE_INTEGRATION_RULE.description.startswith("Authoritative plugin compliance")
