from familyos_cli.plugins.builtin.finance.accounts.account_type import (
    AccountType,
)


def test_account_type_contains_expected_values() -> None:
    assert AccountType.BANK.value == "bank"
    assert AccountType.SAVINGS.value == "savings"
    assert AccountType.INVESTMENT.value == "investment"
    assert AccountType.CASH.value == "cash"
