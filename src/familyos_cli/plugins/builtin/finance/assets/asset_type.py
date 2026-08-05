"""Finance asset types."""

from enum import StrEnum


class AssetType(StrEnum):
    """Supported financial asset types."""

    REAL_ESTATE = "real_estate"
    STOCK = "stock"
    BUSINESS = "business"
    COLLECTIBLE = "collectible"
