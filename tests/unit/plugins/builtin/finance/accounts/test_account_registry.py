from familyos_cli.plugins.builtin.finance.accounts.account import (
    Account,
)
from familyos_cli.plugins.builtin.finance.accounts.account_registry import (
    AccountRegistry,
)
from familyos_cli.plugins.builtin.finance.accounts.account_type import (
    AccountType,
)


def create_account(
    account_id: str = "account-001",
) -> Account:
    return Account(
        id=account_id,
        owner_id="family-001",
        name="Main Account",
        type=AccountType.BANK,
        currency="EUR",
    )


def test_account_registry_adds_accounts() -> None:
    registry = AccountRegistry()

    registry.add(
        create_account(),
    )

    assert len(
        registry.list(),
    ) == 1


def test_account_registry_gets_account_by_id() -> None:
    registry = AccountRegistry()

    registry.add(
        create_account(),
    )

    account = registry.get(
        "account-001",
    )

    assert account is not None
    assert account.id == "account-001"


def test_account_registry_returns_none_for_unknown_id() -> None:
    registry = AccountRegistry()

    assert registry.get(
        "unknown",
    ) is None
