from familyos_cli.plugins.builtin.finance.capabilities.finance_transaction_capability import (
    FinanceTransactionCapability,
)


def test_finance_transaction_capability_has_expected_identifier() -> None:
    capability = FinanceTransactionCapability.create()

    assert str(
        capability.id,
    ) == "familyos.finance.transaction"


def test_finance_transaction_capability_has_finance_metadata() -> None:
    capability = FinanceTransactionCapability.create()

    assert capability.display_name == "Finance Transaction"
    assert capability.metadata["domain"] == "finance"
    assert capability.metadata["version"] == "1.0.0"
