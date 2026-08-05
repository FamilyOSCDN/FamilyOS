from familyos_cli.plugins.builtin.finance.capabilities.finance_liability_capability import (
    FinanceLiabilityCapability,
)


def test_finance_liability_capability_has_expected_identifier() -> None:
    capability = FinanceLiabilityCapability.create()

    assert str(
        capability.id,
    ) == "familyos.finance.liability"


def test_finance_liability_capability_has_finance_metadata() -> None:
    capability = FinanceLiabilityCapability.create()

    assert capability.display_name == "Finance Liability"
    assert capability.metadata["domain"] == "finance"
    assert capability.metadata["version"] == "1.0.0"
