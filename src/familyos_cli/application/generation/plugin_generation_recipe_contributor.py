"""Plugin generation recipe contributor."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
)


class PluginGenerationRecipeContributor:
    """Add plugin generation recipes to a registry."""

    def contribute(
        self,
        registry: GenerationRecipeRegistry,
        contributions: tuple[
            GenerationRecipeContribution,
            ...,
        ],
    ) -> None:
        """Register plugin provided recipes."""

        for contribution in contributions:
            registry.register(
                contribution.recipe,
            )
