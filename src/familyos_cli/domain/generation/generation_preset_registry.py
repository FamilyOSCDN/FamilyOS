"""Generation preset registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_definition import (
    GenerationPresetDefinition,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


class GenerationPresetRegistry:
    """Registry of generation presets."""

    def __init__(
        self,
    ) -> None:
        """Initialize the registry."""

        self._presets: dict[
            GenerationPresetId,
            GenerationPresetDefinition,
        ] = {}

    def register(
        self,
        definition: GenerationPresetDefinition,
    ) -> None:
        """Register a generation preset."""

        preset_id = definition.preset_id()

        if preset_id in self._presets:
            raise ValueError(
                f"Preset '{preset_id}' already registered.",
            )

        self._presets[
            preset_id
        ] = definition

    def get(
        self,
        preset: GenerationPresetId | GenerationPreset,
    ) -> GenerationPresetDefinition:
        """Return a registered preset."""

        preset_id = self._normalize(
            preset,
        )

        try:
            return self._presets[preset_id]

        except KeyError as error:
            raise ValueError(
                f"Preset '{preset_id}' not found.",
            ) from error

    def list(
        self,
    ) -> tuple[GenerationPresetDefinition, ...]:
        """Return all registered presets."""

        return tuple(
            self._presets.values(),
        )

    def _normalize(
        self,
        preset: GenerationPresetId | GenerationPreset,
    ) -> GenerationPresetId:
        """Normalize legacy presets to identifiers."""

        if isinstance(
            preset,
            GenerationPresetId,
        ):
            return preset

        return GenerationPresetId(
            preset.value,
        )
