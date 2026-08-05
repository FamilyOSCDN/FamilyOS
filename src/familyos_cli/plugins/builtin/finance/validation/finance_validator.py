"""Finance validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)
from familyos_cli.plugins.builtin.finance.validation.finance_validation_result import (
    FinanceValidationResult,
)


class FinanceValidator:
    """Validate finance contexts."""

    def validate(
        self,
        context: FinanceContext,
    ) -> FinanceValidationResult:
        """Validate finance context."""

        if (
            context.required_level
            == FinanceLevel.CRITICAL
        ):
            return FinanceValidationResult(
                valid=False,
                message="Critical finance review required.",
            )

        return FinanceValidationResult(
            valid=True,
            message="Finance context validated.",
        )
