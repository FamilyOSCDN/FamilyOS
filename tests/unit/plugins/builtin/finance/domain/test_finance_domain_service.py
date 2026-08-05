"""Tests for FinanceDomainService."""

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_decision import (
    FinanceDecision,
)
from familyos_cli.plugins.builtin.finance.domain.finance_domain_service import (
    FinanceDomainService,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)


def test_standard_finance_level_allows_access() -> None:
    """Standard finance levels should be allowed."""

    service = FinanceDomainService()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.STANDARD,
    )

    decision = service.evaluate(
        context,
    )

    assert decision == FinanceDecision.ALLOW


def test_critical_finance_level_requires_review() -> None:
    """Critical finance levels should require review."""

    service = FinanceDomainService()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.CRITICAL,
    )

    decision = service.evaluate(
        context,
    )

    assert decision == FinanceDecision.REVIEW
