"""Tests for HealthRuleEvaluator."""

from familyos_cli.plugins.builtin.health.domain.health_context import (
    HealthContext,
)
from familyos_cli.plugins.builtin.health.domain.health_decision import (
    HealthDecision,
)
from familyos_cli.plugins.builtin.health.domain.health_level import (
    HealthLevel,
)
from familyos_cli.plugins.builtin.health.rules.health_rule import (
    HealthRule,
)
from familyos_cli.plugins.builtin.health.rules.health_rule_evaluator import (
    HealthRuleEvaluator,
)


def create_rule() -> HealthRule:
    """Create a test health rule."""

    return HealthRule(
        id="health.rule.basic",
        name="Basic Health Rule",
        version="1.0.0",
        severity="LOW",
    )


def test_standard_health_rule_allows_access() -> None:
    """Standard health level should be allowed."""

    evaluator = HealthRuleEvaluator()

    context = HealthContext(
        domain_name="family",
        subject="member",
        required_level=HealthLevel.STANDARD,
    )

    decision = evaluator.evaluate(
        create_rule(),
        context,
    )

    assert decision == HealthDecision.ALLOW


def test_critical_health_rule_requires_review() -> None:
    """Critical health level should require review."""

    evaluator = HealthRuleEvaluator()

    context = HealthContext(
        domain_name="family",
        subject="member",
        required_level=HealthLevel.CRITICAL,
    )

    decision = evaluator.evaluate(
        create_rule(),
        context,
    )

    assert decision == HealthDecision.REVIEW
