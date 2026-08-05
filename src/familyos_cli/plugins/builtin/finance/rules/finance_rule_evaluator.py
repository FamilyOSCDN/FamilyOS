"""Finance rule evaluator."""

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
from familyos_cli.plugins.builtin.finance.rules.finance_rule import (
    FinanceRule,
)


class FinanceRuleEvaluator:
    """Evaluate finance rules."""

    def evaluate(
        self,
        rule: FinanceRule,
        context: FinanceContext,
    ) -> FinanceDecision:
        """Evaluate a finance rule."""

        if (
            context.required_level
            == FinanceLevel.CRITICAL
        ):
            return FinanceDecision.REVIEW

        return FinanceDecision.ALLOW
