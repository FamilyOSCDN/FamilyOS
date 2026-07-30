"""Generation catalog."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_catalog_entry import (
    GenerationCatalogEntry,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


class GenerationCatalog:
    """Catalog of discoverable generation presets."""

    def __init__(
        self,
    ) -> None:
        """Initialize the catalog."""

        self._entries: dict[
            GenerationPresetId,
            GenerationCatalogEntry,
        ] = {}

    def register(
        self,
        entry: GenerationCatalogEntry,
    ) -> None:
        """Register a catalog entry."""

        preset_id = self._normalize_preset_id(
            entry.preset,
        )

        if preset_id in self._entries:
            raise ValueError(
                f"Preset '{preset_id}' already registered.",
            )

        self._entries[preset_id] = entry

    def get(
        self,
        preset: GenerationPresetId | object,
    ) -> GenerationCatalogEntry:
        """Return a catalog entry."""

        preset_id = self._normalize_preset_id(
            preset,
        )

        try:
            return self._entries[preset_id]

        except KeyError as error:
            raise ValueError(
                f"Preset '{preset_id}' not found.",
            ) from error

    def list(
        self,
    ) -> tuple[GenerationCatalogEntry, ...]:
        """Return all catalog entries."""

        return tuple(
            self._entries.values(),
        )

    @staticmethod
    def _normalize_preset_id(
        preset: GenerationPresetId | object,
    ) -> GenerationPresetId:
        """Normalize preset identifiers."""

        if isinstance(
            preset,
            GenerationPresetId,
        ):
            return preset

        value = getattr(
            preset,
            "value",
            None,
        )

        if isinstance(
            value,
            str,
        ):
            return GenerationPresetId(
                value,
            )

        raise ValueError(
            f"Invalid generation preset '{preset}'.",
        )
