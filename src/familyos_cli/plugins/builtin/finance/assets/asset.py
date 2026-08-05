"""Finance asset entity."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from familyos_cli.plugins.builtin.finance.assets.asset_type import (
    AssetType,
)


@dataclass(frozen=True, slots=True)
class Asset:
    """Represents a family financial asset."""

    id: str
    owner_id: str
    name: str
    type: AssetType
    estimated_value: Decimal
    currency: str

    def __post_init__(
        self,
    ) -> None:
        """Validate asset invariants."""

        if not self.id:
            raise ValueError(
                "Asset id cannot be empty.",
            )

        if not self.owner_id:
            raise ValueError(
                "Asset owner id cannot be empty.",
            )

        if not self.name:
            raise ValueError(
                "Asset name cannot be empty.",
            )

        if self.estimated_value < Decimal("0"):
            raise ValueError(
                "Asset estimated value cannot be negative.",
            )

        if not self.currency:
            raise ValueError(
                "Asset currency cannot be empty.",
            )
