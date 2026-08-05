from familyos_cli.plugins.builtin.finance.capabilities.finance_account_capability import (
    FinanceAccountCapability,
)


def test_finance_account_capability_has_expected_identifier() -> None:
    capability = FinanceAccountCapability.create()

    assert str(
        capability.id,
    ) == "familyos.finance.account"


def test_finance_account_capability_has_finance_metadata() -> None:
    capability = FinanceAccountCapability.create()

    assert capability.display_name == "Finance Account"
    assert capability.metadata["domain"] == "finance"
    assert capability.metadata["version"] == "1.0.0"
