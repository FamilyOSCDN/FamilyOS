from datetime import date
from decimal import Decimal

import pytest

from familyos_cli.plugins.builtin.finance.transactions.transaction import (
    Transaction,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction_registry import (
    TransactionRegistry,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction_type import (
    TransactionType,
)


def create_transaction(
    transaction_id: str = "transaction-001",
) -> Transaction:
    return Transaction(
        id=transaction_id,
        account_id="account-001",
        amount=Decimal("100.00"),
        currency="EUR",
        type=TransactionType.INCOME,
        date=date(2026, 8, 3),
        category="salary",
    )


def test_transaction_registry_adds_transactions() -> None:
    registry = TransactionRegistry()

    registry.add(
        create_transaction(),
    )

    assert len(
        registry.list(),
    ) == 1


def test_transaction_registry_gets_transaction_by_id() -> None:
    registry = TransactionRegistry()

    registry.add(
        create_transaction(),
    )

    transaction = registry.get(
        "transaction-001",
    )

    assert transaction is not None
    assert transaction.id == "transaction-001"


def test_transaction_registry_returns_none_for_unknown_id() -> None:
    registry = TransactionRegistry()

    assert registry.get(
        "unknown",
    ) is None


def test_transaction_registry_rejects_duplicate_id() -> None:
    registry = TransactionRegistry()

    transaction = create_transaction()

    registry.add(
        transaction,
    )

    with pytest.raises(
        ValueError,
        match="Transaction 'transaction-001' already exists",
    ):
        registry.add(
            create_transaction(),
        )

    assert registry.list() == [
        transaction,
    ]
