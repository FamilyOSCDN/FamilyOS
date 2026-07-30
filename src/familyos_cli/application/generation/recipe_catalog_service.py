"""Generation recipe catalog service."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_recipe import (
    GenerationRecipe,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)


class RecipeCatalogService:
    """Provide access to registered generation recipes."""

    def __init__(
        self,
        registry: GenerationRecipeRegistry,
    ) -> None:
        """Initialize the recipe catalog service."""

        self._registry = registry

    def list_recipes(
        self,
    ) -> tuple[GenerationRecipe, ...]:
        """Return all available generation recipes."""

        return self._registry.list()
