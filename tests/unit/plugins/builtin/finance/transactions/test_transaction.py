from datetime import date
from decimal import Decimal

from pytest import raises

from familyos_cli.plugins.builtin.finance.transactions.transaction import (
    Transaction,
)
from familyos_cli.plugins.builtin.finance.transactions.transaction_type import (
    TransactionType,
)


def create_transaction(
    amount: Decimal = Decimal("100.00"),
) -> Transaction:
    return Transaction(
        id="transaction-001",
        account_id="account-001",
        amount=amount,
        currency="EUR",
        type=TransactionType.INCOME,
        date=date(2026, 8, 3),
        category="salary",
        description="Monthly salary",
    )


def test_transaction_can_be_created() -> None:
    transaction = create_transaction()

    assert transaction.id == "transaction-001"
    assert transaction.account_id == "account-001"
    assert transaction.amount == Decimal("100.00")
    assert transaction.currency == "EUR"
    assert transaction.type == TransactionType.INCOME


def test_transaction_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Transaction id cannot be empty.",
    ):
        Transaction(
            id="",
            account_id="account-001",
            amount=Decimal("100.00"),
            currency="EUR",
            type=TransactionType.INCOME,
            date=date(2026, 8, 3),
            category="salary",
        )


def test_transaction_rejects_empty_account_id() -> None:
    with raises(
        ValueError,
        match="Transaction account id cannot be empty.",
    ):
        Transaction(
            id="transaction-001",
            account_id="",
            amount=Decimal("100.00"),
            currency="EUR",
            type=TransactionType.INCOME,
            date=date(2026, 8, 3),
            category="salary",
        )


def test_transaction_rejects_non_positive_amount() -> None:
    with raises(
        ValueError,
        match="Transaction amount must be positive.",
    ):
        create_transaction(
            Decimal("0"),
        )


def test_transaction_rejects_empty_currency() -> None:
    with raises(
        ValueError,
        match="Transaction currency cannot be empty.",
    ):
        Transaction(
            id="transaction-001",
            account_id="account-001",
            amount=Decimal("100.00"),
            currency="",
            type=TransactionType.INCOME,
            date=date(2026, 8, 3),
            category="salary",
        )


def test_transaction_rejects_empty_category() -> None:
    with raises(
        ValueError,
        match="Transaction category cannot be empty.",
    ):
        Transaction(
            id="transaction-001",
            account_id="account-001",
            amount=Decimal("100.00"),
            currency="EUR",
            type=TransactionType.INCOME,
            date=date(2026, 8, 3),
            category="",
        )
