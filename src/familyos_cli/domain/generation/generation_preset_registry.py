"""Generation preset registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_definition import (
    GenerationPresetDefinition,
)


class GenerationPresetRegistry:
    """Registry of generation presets."""

    def __init__(
        self,
    ) -> None:
        """Initialize the registry."""

        self._presets: dict[
            GenerationPreset,
            GenerationPresetDefinition,
        ] = {}

    def register(
        self,
        definition: GenerationPresetDefinition,
    ) -> None:
        """Register a generation preset."""

        if definition.preset in self._presets:
            raise ValueError(
                f"Preset '{definition.preset}' already registered.",
            )

        self._presets[definition.preset] = definition

    def get(
        self,
        preset: GenerationPreset,
    ) -> GenerationPresetDefinition:
        """Return a registered preset."""

        try:
            return self._presets[preset]
        except KeyError as error:
            raise ValueError(
                f"Preset '{preset}' not found.",
            ) from error

    def list(
        self,
    ) -> tuple[GenerationPresetDefinition, ...]:
        """Return all registered presets."""

        return tuple(
            self._presets.values(),
        )
