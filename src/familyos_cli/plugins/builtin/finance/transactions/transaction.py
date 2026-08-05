"""Finance transaction entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from familyos_cli.plugins.builtin.finance.transactions.transaction_type import (
    TransactionType,
)


@dataclass(frozen=True, slots=True)
class Transaction:
    """Represents a financial transaction."""

    id: str
    account_id: str
    amount: Decimal
    currency: str
    type: TransactionType
    date: date
    category: str
    description: str = ""

    def __post_init__(
        self,
    ) -> None:
        """Validate transaction invariants."""

        if not self.id:
            raise ValueError(
                "Transaction id cannot be empty.",
            )

        if not self.account_id:
            raise ValueError(
                "Transaction account id cannot be empty.",
            )

        if self.amount <= Decimal("0"):
            raise ValueError(
                "Transaction amount must be positive.",
            )

        if not self.currency:
            raise ValueError(
                "Transaction currency cannot be empty.",
            )

        if not self.category:
            raise ValueError(
                "Transaction category cannot be empty.",
            )
