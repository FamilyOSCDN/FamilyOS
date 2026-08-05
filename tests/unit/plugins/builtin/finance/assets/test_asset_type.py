from familyos_cli.plugins.builtin.finance.assets.asset_type import (
    AssetType,
)


def test_asset_type_contains_expected_values() -> None:
    assert AssetType.REAL_ESTATE.value == "real_estate"
    assert AssetType.STOCK.value == "stock"
    assert AssetType.BUSINESS.value == "business"
    assert AssetType.COLLECTIBLE.value == "collectible"
