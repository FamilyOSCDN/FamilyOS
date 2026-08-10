"""Plugin identity services."""

from .plugin_id_normalizer import (
    LEGACY_PLUGIN_ID_ALIASES,
    normalize_plugin_id,
)

__all__ = [
    "LEGACY_PLUGIN_ID_ALIASES",
    "normalize_plugin_id",
]
