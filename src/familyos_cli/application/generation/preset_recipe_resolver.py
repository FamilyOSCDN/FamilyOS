"""Preset recipe resolver."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.domain.generation.generation_preset_resolver import (
    GenerationPresetResolver,
)


class PresetRecipeResolver:
    """Resolve a recipe name from a generation preset."""

    def __init__(
        self,
        resolver: GenerationPresetResolver,
    ) -> None:
        """Initialize resolver."""

        self._resolver = resolver

    def resolve(
        self,
        preset: GenerationPresetId | GenerationPreset,
    ) -> str:
        """Resolve the recipe name for a preset."""

        definition = self._resolver.resolve(
            preset,
        )

        if not definition.recipes:
            raise ValueError(
                f"Preset '{preset}' has no recipes.",
            )

        return definition.recipes[0]
