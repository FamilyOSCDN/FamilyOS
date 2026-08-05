from familyos_cli.plugins.builtin.finance.capabilities.finance_asset_capability import (
    FinanceAssetCapability,
)


def test_finance_asset_capability_has_expected_identifier() -> None:
    capability = FinanceAssetCapability.create()

    assert str(
        capability.id,
    ) == "familyos.finance.asset"


def test_finance_asset_capability_has_finance_metadata() -> None:
    capability = FinanceAssetCapability.create()

    assert capability.display_name == "Finance Asset"
    assert capability.metadata["domain"] == "finance"
    assert capability.metadata["version"] == "1.0.0"
