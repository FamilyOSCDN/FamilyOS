"""Default generation recipe registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)


class DefaultRecipeRegistry:
    """Create the default generation recipe registry."""

    @staticmethod
    def create() -> GenerationRecipeRegistry:
        """Create a registry with built-in recipes."""

        registry = GenerationRecipeRegistry()

        registry.register(
            DomainDocumentationRecipe(),
        )

        return registry
