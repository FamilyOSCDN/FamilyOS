"""Application recipe registry factory."""

from __future__ import annotations

from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)
from familyos_cli.application.generation.plugin_generation_recipe_contributor import (
    PluginGenerationRecipeContributor,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
)


class ApplicationRecipeRegistryFactory:
    """Create application generation recipe registries."""

    @staticmethod
    def create(
        contributions: tuple[
            GenerationRecipeContribution,
            ...,
        ] = (),
    ) -> GenerationRecipeRegistry:
        """Create registry with built-in and plugin recipes."""

        registry = DefaultRecipeRegistry.create()

        PluginGenerationRecipeContributor().contribute(
            registry,
            contributions,
        )

        return registry
