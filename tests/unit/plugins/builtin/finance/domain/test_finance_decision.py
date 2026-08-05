"""Tests for FinanceDecision."""

from familyos_cli.plugins.builtin.finance.domain.finance_decision import (
    FinanceDecision,
)


def test_finance_decision_values() -> None:
    """Finance decisions expose expected values."""

    assert FinanceDecision.ALLOW.value == "allow"
    assert FinanceDecision.REVIEW.value == "review"
    assert FinanceDecision.DENY.value == "deny"
