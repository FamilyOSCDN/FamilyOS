"""Tests for SecurityRuleEvaluator."""

from familyos_cli.plugins.builtin.security.domain.security_context import (
    SecurityContext,
)
from familyos_cli.plugins.builtin.security.domain.security_decision import (
    SecurityDecision,
)
from familyos_cli.plugins.builtin.security.domain.security_level import (
    SecurityLevel,
)
from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)
from familyos_cli.plugins.builtin.security.rules.security_rule_evaluator import (
    SecurityRuleEvaluator,
)


def create_rule(
    severity: str = "LOW",
) -> SecurityRule:
    """Create a test security rule."""

    return SecurityRule(
        id="security.rule.test",
        name="Test Security Rule",
        version="1.0.0",
        severity=severity,
        description="Test rule.",
    )


def test_high_security_rule_allows_access() -> None:
    """Standard rules should allow access."""

    evaluator = SecurityRuleEvaluator()

    context = SecurityContext(
        domain_name="family",
        resource="profile",
        required_level=SecurityLevel.HIGH,
    )

    decision = evaluator.evaluate(
        create_rule("HIGH"),
        context,
    )

    assert decision == SecurityDecision.ALLOW


def test_critical_rule_requires_review() -> None:
    """Critical rules require review."""

    evaluator = SecurityRuleEvaluator()

    context = SecurityContext(
        domain_name="family",
        resource="identity",
        required_level=SecurityLevel.HIGH,
    )

    decision = evaluator.evaluate(
        create_rule("CRITICAL"),
        context,
    )

    assert decision == SecurityDecision.REVIEW
