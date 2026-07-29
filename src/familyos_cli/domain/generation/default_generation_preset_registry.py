"""Default generation preset registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_definition import (
    GenerationPresetDefinition,
)
from familyos_cli.domain.generation.generation_preset_registry import (
    GenerationPresetRegistry,
)


class DefaultGenerationPresetRegistry:
    """Create the default generation preset registry."""

    @staticmethod
    def create() -> GenerationPresetRegistry:
        """Create registry with default presets."""

        registry = GenerationPresetRegistry()

        registry.register(
            GenerationPresetDefinition(
                preset=GenerationPreset.MINIMAL,
                recipes=(
                    "domain_documentation",
                ),
            ),
        )

        registry.register(
            GenerationPresetDefinition(
                preset=GenerationPreset.STANDARD,
                recipes=(
                    "domain_documentation",
                    "entity_documentation",
                    "aggregate_documentation",
                ),
            ),
        )

        registry.register(
            GenerationPresetDefinition(
                preset=GenerationPreset.COMPLETE,
                recipes=(
                    "full_domain_documentation",
                ),
            ),
        )

        return registry
