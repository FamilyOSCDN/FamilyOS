from pytest import raises

from familyos_cli.plugins.builtin.finance.accounts.account import (
    Account,
)
from familyos_cli.plugins.builtin.finance.accounts.account_status import (
    AccountStatus,
)
from familyos_cli.plugins.builtin.finance.accounts.account_type import (
    AccountType,
)


def test_account_can_be_created() -> None:
    account = Account(
        id="account-001",
        owner_id="family-001",
        name="Main Bank Account",
        type=AccountType.BANK,
        currency="EUR",
    )

    assert account.id == "account-001"
    assert account.owner_id == "family-001"
    assert account.name == "Main Bank Account"
    assert account.type == AccountType.BANK
    assert account.currency == "EUR"
    assert account.status == AccountStatus.ACTIVE


def test_account_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Account id cannot be empty.",
    ):
        Account(
            id="",
            owner_id="family-001",
            name="Main Bank Account",
            type=AccountType.BANK,
            currency="EUR",
        )


def test_account_rejects_empty_owner_id() -> None:
    with raises(
        ValueError,
        match="Account owner id cannot be empty.",
    ):
        Account(
            id="account-001",
            owner_id="",
            name="Main Bank Account",
            type=AccountType.BANK,
            currency="EUR",
        )


def test_account_rejects_empty_name() -> None:
    with raises(
        ValueError,
        match="Account name cannot be empty.",
    ):
        Account(
            id="account-001",
            owner_id="family-001",
            name="",
            type=AccountType.BANK,
            currency="EUR",
        )


def test_account_rejects_empty_currency() -> None:
    with raises(
        ValueError,
        match="Account currency cannot be empty.",
    ):
        Account(
            id="account-001",
            owner_id="family-001",
            name="Main Bank Account",
            type=AccountType.BANK,
            currency="",
        )
