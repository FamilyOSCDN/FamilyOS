"""Tests for FinanceRuleEvaluator."""

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_decision import (
    FinanceDecision,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)
from familyos_cli.plugins.builtin.finance.rules.finance_rule import (
    FinanceRule,
)
from familyos_cli.plugins.builtin.finance.rules.finance_rule_evaluator import (
    FinanceRuleEvaluator,
)


def create_rule() -> FinanceRule:
    """Create a test finance rule."""

    return FinanceRule(
        id="finance.rule.basic",
        name="Basic Finance Rule",
        version="1.0.0",
        severity="LOW",
    )


def test_standard_finance_rule_allows_access() -> None:
    """Standard finance levels should be allowed."""

    evaluator = FinanceRuleEvaluator()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.STANDARD,
    )

    decision = evaluator.evaluate(
        create_rule(),
        context,
    )

    assert decision == FinanceDecision.ALLOW


def test_critical_finance_rule_requires_review() -> None:
    """Critical finance levels should require review."""

    evaluator = FinanceRuleEvaluator()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.CRITICAL,
    )

    decision = evaluator.evaluate(
        create_rule(),
        context,
    )

    assert decision == FinanceDecision.REVIEW
