"""Finance budget entity."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from familyos_cli.plugins.builtin.finance.budgets.budget_category import (
    BudgetCategory,
)


@dataclass(frozen=True, slots=True)
class Budget:
    """Represents a family financial budget."""

    id: str
    owner_id: str
    name: str
    category: BudgetCategory
    limit_amount: Decimal
    currency: str
    period: str

    def __post_init__(
        self,
    ) -> None:
        """Validate budget invariants."""

        if not self.id:
            raise ValueError(
                "Budget id cannot be empty.",
            )

        if not self.owner_id:
            raise ValueError(
                "Budget owner id cannot be empty.",
            )

        if not self.name:
            raise ValueError(
                "Budget name cannot be empty.",
            )

        if self.limit_amount <= Decimal("0"):
            raise ValueError(
                "Budget limit amount must be positive.",
            )

        if not self.currency:
            raise ValueError(
                "Budget currency cannot be empty.",
            )

        if not self.period:
            raise ValueError(
                "Budget period cannot be empty.",
            )
