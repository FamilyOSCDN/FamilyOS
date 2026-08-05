from familyos_cli.plugins.builtin.finance.transactions.transaction_type import (
    TransactionType,
)


def test_transaction_type_contains_expected_values() -> None:
    assert TransactionType.INCOME.value == "income"
    assert TransactionType.EXPENSE.value == "expense"
    assert TransactionType.TRANSFER.value == "transfer"
    assert TransactionType.INVESTMENT.value == "investment"
