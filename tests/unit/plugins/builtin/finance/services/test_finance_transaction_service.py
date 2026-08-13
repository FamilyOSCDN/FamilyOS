"""Tests for FinanceTransactionService."""

from datetime import date
from decimal import Decimal

import pytest

from familyos_cli.plugins.builtin.finance.accounts.account import (
    Account,
)
from familyos_cli.plugins.builtin.finance.accounts.account_registry import (
    AccountRegistry,
)
from familyos_cli.plugins.builtin.finance.accounts.account_type import (
    AccountType,
)
from familyos_cli.plugins.builtin.finance.services import (
    FinanceTransactionService,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction import (
    Transaction,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction_registry import (
    TransactionRegistry,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction_type import (
    TransactionType,
)


def create_account(
    *,
    account_id: str = "account-001",
    currency: str = "EUR",
) -> Account:
    """Create a finance account."""

    return Account(
        id=account_id,
        owner_id="family-001",
        name="Main Account",
        type=AccountType.BANK,
        currency=currency,
    )


def create_transaction(
    *,
    transaction_id: str = "transaction-001",
    account_id: str = "account-001",
    currency: str = "EUR",
) -> Transaction:
    """Create a financial transaction."""

    return Transaction(
        id=transaction_id,
        account_id=account_id,
        amount=Decimal("100.00"),
        currency=currency,
        type=TransactionType.INCOME,
        date=date(2026, 8, 13),
        category="salary",
        description="Monthly salary",
    )


def create_service(
) -> tuple[
    FinanceTransactionService,
    AccountRegistry,
    TransactionRegistry,
]:
    """Create a service with isolated registries."""

    accounts = AccountRegistry()
    transactions = TransactionRegistry()

    return (
        FinanceTransactionService(
            account_registry=accounts,
            transaction_registry=transactions,
        ),
        accounts,
        transactions,
    )


def test_registers_transaction_for_existing_account() -> None:
    """Valid transactions should be registered."""

    service, accounts, transactions = create_service()

    account = create_account()
    transaction = create_transaction()

    accounts.add(
        account,
    )

    registered = service.register(
        transaction,
    )

    assert registered == transaction

    assert transactions.get(
        transaction.id,
    ) == transaction

    assert transactions.list() == [
        transaction,
    ]


def test_rejects_transaction_for_unknown_account() -> None:
    """Transactions must reference an existing account."""

    service, _, transactions = create_service()

    transaction = create_transaction(
        account_id="unknown-account",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Transaction account does not exist: "
            "unknown-account"
        ),
    ):
        service.register(
            transaction,
        )

    assert transactions.list() == []


def test_rejects_transaction_with_mismatched_currency() -> None:
    """Transaction currency must match account currency."""

    service, accounts, transactions = create_service()

    accounts.add(
        create_account(
            currency="EUR",
        ),
    )

    transaction = create_transaction(
        currency="USD",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Transaction currency does not match "
            "account currency: USD != EUR"
        ),
    ):
        service.register(
            transaction,
        )

    assert transactions.list() == []


def test_registers_multiple_transactions_for_same_account() -> None:
    """One account may receive multiple valid transactions."""

    service, accounts, transactions = create_service()

    accounts.add(
        create_account(),
    )

    first = create_transaction(
        transaction_id="transaction-001",
    )

    second = create_transaction(
        transaction_id="transaction-002",
    )

    service.register(
        first,
    )

    service.register(
        second,
    )

    assert transactions.list() == [
        first,
        second,
    ]
