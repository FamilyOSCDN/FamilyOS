"""Finance transaction application service."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.accounts.account_registry import (
    AccountRegistry,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction import (
    Transaction,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction_registry import (
    TransactionRegistry,
)


class FinanceTransactionService:
    """Coordinate financial transaction registration."""

    def __init__(
        self,
        account_registry: AccountRegistry,
        transaction_registry: TransactionRegistry,
    ) -> None:
        """Initialize transaction orchestration."""

        self._account_registry = account_registry
        self._transaction_registry = transaction_registry

    def register(
        self,
        transaction: Transaction,
    ) -> Transaction:
        """Validate and register a financial transaction."""

        account = self._account_registry.get(
            transaction.account_id,
        )

        if account is None:
            raise ValueError(
                "Transaction account does not exist: "
                f"{transaction.account_id}.",
            )

        if transaction.currency != account.currency:
            raise ValueError(
                "Transaction currency does not match "
                "account currency: "
                f"{transaction.currency} != "
                f"{account.currency}.",
            )

        self._transaction_registry.add(
            transaction,
        )

        return transaction
