"""Finance transaction registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.transactions.transaction import (
    Transaction,
)


class TransactionRegistry:
    """Store financial transactions."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._transactions: list[Transaction] = []

    def add(
        self,
        transaction: Transaction,
    ) -> None:
        """Add a transaction."""

        self._transactions.append(
            transaction,
        )

    def list(
        self,
    ) -> list[Transaction]:
        """Return all transactions."""

        return list(
            self._transactions,
        )

    def get(
        self,
        transaction_id: str,
    ) -> Transaction | None:
        """Return transaction by identifier."""

        return next(
            (
                transaction
                for transaction in self._transactions
                if transaction.id == transaction_id
            ),
            None,
        )
