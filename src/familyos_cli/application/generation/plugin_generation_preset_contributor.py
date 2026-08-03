"""Plugin generation preset contributor."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_preset_definition import (
    GenerationPresetDefinition,
)
from familyos_cli.domain.generation.generation_preset_registry import (
    GenerationPresetRegistry,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)


class PluginGenerationPresetContributor:
    """Register plugin generation presets."""

    def contribute(
        self,
        registry: GenerationPresetRegistry,
        contributions: tuple[
            GenerationContribution,
            ...,
        ],
    ) -> None:
        """Add plugin presets to the registry."""

        for contribution in contributions:
            registry.register(
                GenerationPresetDefinition(
                    preset=contribution.preset,
                    recipes=contribution.recipes,
                ),
            )
