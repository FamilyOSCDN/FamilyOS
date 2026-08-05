"""Finance domain service."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_decision import (
    FinanceDecision,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)


class FinanceDomainService:
    """Domain service for finance decisions."""

    def evaluate(
        self,
        context: FinanceContext,
    ) -> FinanceDecision:
        """Evaluate finance context."""

        if (
            context.required_level
            == FinanceLevel.CRITICAL
        ):
            return FinanceDecision.REVIEW

        return FinanceDecision.ALLOW
