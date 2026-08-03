"""Generation preset resolver."""

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
from familyos_cli.domain.generation.generation_preset_registry import (
    GenerationPresetRegistry,
)


class GenerationPresetResolver:
    """Resolve generation presets."""

    def __init__(
        self,
        registry: GenerationPresetRegistry,
    ) -> None:
        """Initialize the resolver."""

        self._registry = registry

    def resolve(
        self,
        preset: GenerationPresetId | GenerationPreset,
    ) -> GenerationPresetDefinition:
        """Resolve a preset definition."""

        return self._registry.get(
            preset,
        )
