from decimal import Decimal

from pytest import raises

from familyos_cli.plugins.builtin.finance.assets.asset import (
    Asset,
)
from familyos_cli.plugins.builtin.finance.assets.asset_type import (
    AssetType,
)


def create_asset(
    value: Decimal = Decimal("10000.00"),
) -> Asset:
    return Asset(
        id="asset-001",
        owner_id="family-001",
        name="Family Apartment",
        type=AssetType.REAL_ESTATE,
        estimated_value=value,
        currency="EUR",
    )


def test_asset_can_be_created() -> None:
    asset = create_asset()

    assert asset.id == "asset-001"
    assert asset.owner_id == "family-001"
    assert asset.name == "Family Apartment"
    assert asset.type == AssetType.REAL_ESTATE
    assert asset.estimated_value == Decimal(
        "10000.00",
    )
    assert asset.currency == "EUR"


def test_asset_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Asset id cannot be empty.",
    ):
        Asset(
            id="",
            owner_id="family-001",
            name="Apartment",
            type=AssetType.REAL_ESTATE,
            estimated_value=Decimal("10000"),
            currency="EUR",
        )


def test_asset_rejects_empty_owner_id() -> None:
    with raises(
        ValueError,
        match="Asset owner id cannot be empty.",
    ):
        Asset(
            id="asset-001",
            owner_id="",
            name="Apartment",
            type=AssetType.REAL_ESTATE,
            estimated_value=Decimal("10000"),
            currency="EUR",
        )


def test_asset_rejects_empty_name() -> None:
    with raises(
        ValueError,
        match="Asset name cannot be empty.",
    ):
        Asset(
            id="asset-001",
            owner_id="family-001",
            name="",
            type=AssetType.REAL_ESTATE,
            estimated_value=Decimal("10000"),
            currency="EUR",
        )


def test_asset_rejects_negative_value() -> None:
    with raises(
        ValueError,
        match="Asset estimated value cannot be negative.",
    ):
        create_asset(
            Decimal("-1"),
        )


def test_asset_rejects_empty_currency() -> None:
    with raises(
        ValueError,
        match="Asset currency cannot be empty.",
    ):
        Asset(
            id="asset-001",
            owner_id="family-001",
            name="Apartment",
            type=AssetType.REAL_ESTATE,
            estimated_value=Decimal("10000"),
            currency="",
        )
