"""Generation catalog entry."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


@dataclass(frozen=True, slots=True)
class GenerationCatalogEntry:
    """Describe a discoverable generation preset."""

    preset: GenerationPresetId

    description: str

    recipes: tuple[str, ...]
