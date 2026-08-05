"""Tests for FinancePolicyEvaluator."""

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_decision import (
    FinanceDecision,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)
from familyos_cli.plugins.builtin.finance.policies.finance_policy import (
    FinancePolicy,
)
from familyos_cli.plugins.builtin.finance.policies.finance_policy_evaluator import (
    FinancePolicyEvaluator,
)


def create_policy() -> FinancePolicy:
    """Create a test finance policy."""

    return FinancePolicy(
        id="finance.policy.basic",
        name="Basic Finance Policy",
        version="1.0.0",
    )


def test_standard_finance_policy_allows_access() -> None:
    """Standard finance levels should be allowed."""

    evaluator = FinancePolicyEvaluator()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.STANDARD,
    )

    decision = evaluator.evaluate(
        create_policy(),
        context,
    )

    assert decision == FinanceDecision.ALLOW


def test_critical_finance_policy_requires_review() -> None:
    """Critical finance levels should require review."""

    evaluator = FinancePolicyEvaluator()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.CRITICAL,
    )

    decision = evaluator.evaluate(
        create_policy(),
        context,
    )

    assert decision == FinanceDecision.REVIEW
