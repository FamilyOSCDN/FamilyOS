"""Generation catalog."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_catalog_entry import (
    GenerationCatalogEntry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


class GenerationCatalog:
    """Catalog of discoverable generation presets."""

    def __init__(
        self,
    ) -> None:
        """Initialize the catalog."""

        self._entries: dict[
            GenerationPreset,
            GenerationCatalogEntry,
        ] = {}

    def register(
        self,
        entry: GenerationCatalogEntry,
    ) -> None:
        """Register a catalog entry."""

        if entry.preset in self._entries:
            raise ValueError(
                f"Preset '{entry.preset}' already registered.",
            )

        self._entries[entry.preset] = entry

    def get(
        self,
        preset: GenerationPreset,
    ) -> GenerationCatalogEntry:
        """Return a catalog entry."""

        try:
            return self._entries[preset]

        except KeyError as error:
            raise ValueError(
                f"Preset '{preset}' not found.",
            ) from error

    def list(
        self,
    ) -> tuple[GenerationCatalogEntry, ...]:
        """Return all catalog entries."""

        return tuple(
            self._entries.values(),
        )
