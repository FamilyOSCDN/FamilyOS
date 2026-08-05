"""Finance policy evaluator."""

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
from familyos_cli.plugins.builtin.finance.policies.finance_policy import (
    FinancePolicy,
)


class FinancePolicyEvaluator:
    """Evaluate finance policies."""

    def evaluate(
        self,
        policy: FinancePolicy,
        context: FinanceContext,
    ) -> FinanceDecision:
        """Evaluate a finance policy."""

        if (
            context.required_level
            == FinanceLevel.CRITICAL
        ):
            return FinanceDecision.REVIEW

        return FinanceDecision.ALLOW
