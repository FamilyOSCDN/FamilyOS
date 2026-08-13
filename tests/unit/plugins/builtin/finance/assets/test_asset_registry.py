from decimal import Decimal

import pytest

from familyos_cli.plugins.builtin.finance.assets.asset import (
    Asset,
)
from familyos_cli.plugins.builtin.finance.assets.asset_registry import (
    AssetRegistry,
)
from familyos_cli.plugins.builtin.finance.assets.asset_type import (
    AssetType,
)


def create_asset(
    asset_id: str = "asset-001",
) -> Asset:
    return Asset(
        id=asset_id,
        owner_id="family-001",
        name="Family Apartment",
        type=AssetType.REAL_ESTATE,
        estimated_value=Decimal("10000"),
        currency="EUR",
    )


def test_asset_registry_adds_assets() -> None:
    registry = AssetRegistry()

    registry.add(
        create_asset(),
    )

    assert len(
        registry.list(),
    ) == 1


def test_asset_registry_gets_asset_by_id() -> None:
    registry = AssetRegistry()

    registry.add(
        create_asset(),
    )

    asset = registry.get(
        "asset-001",
    )

    assert asset is not None
    assert asset.id == "asset-001"


def test_asset_registry_returns_none_for_unknown_id() -> None:
    registry = AssetRegistry()

    assert registry.get(
        "unknown",
    ) is None


def test_asset_registry_rejects_duplicate_id() -> None:
    registry = AssetRegistry()

    asset = create_asset()

    registry.add(
        asset,
    )

    with pytest.raises(
        ValueError,
        match="Asset 'asset-001' already exists",
    ):
        registry.add(
            create_asset(),
        )

    assert registry.list() == [
        asset,
    ]
