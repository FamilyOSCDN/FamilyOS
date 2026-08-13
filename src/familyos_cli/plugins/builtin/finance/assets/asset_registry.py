"""Finance asset registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.assets.asset import (
    Asset,
)


class AssetRegistry:
    """Store financial assets."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._assets: list[Asset] = []

    def add(
        self,
        asset: Asset,
    ) -> None:
        """Add an asset."""

        if self.get(asset.id) is not None:
            raise ValueError(
                f"Asset '{asset.id}' already exists.",
            )

        self._assets.append(
            asset,
        )

    def list(
        self,
    ) -> list[Asset]:
        """Return all assets."""

        return list(
            self._assets,
        )

    def get(
        self,
        asset_id: str,
    ) -> Asset | None:
        """Return asset by identifier."""

        return next(
            (
                asset
                for asset in self._assets
                if asset.id == asset_id
            ),
            None,
        )
