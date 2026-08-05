from familyos_cli.plugins.builtin.finance.accounts.account_status import (
    AccountStatus,
)


def test_account_status_contains_expected_values() -> None:
    assert AccountStatus.ACTIVE.value == "active"
    assert AccountStatus.INACTIVE.value == "inactive"
    assert AccountStatus.CLOSED.value == "closed"
