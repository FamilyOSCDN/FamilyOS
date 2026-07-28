"""Generation recipe registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_recipe import (
    GenerationRecipe,
)


class GenerationRecipeRegistry:
    """Registry of generation recipes."""

    def __init__(
        self,
    ) -> None:
        """Initialize the registry."""

        self._recipes: dict[str, GenerationRecipe] = {}

    def register(
        self,
        recipe: GenerationRecipe,
    ) -> None:
        """Register a generation recipe."""

        if recipe.name in self._recipes:
            raise ValueError(
                f"Recipe '{recipe.name}' already registered.",
            )

        self._recipes[recipe.name] = recipe

    def get(
        self,
        name: str,
    ) -> GenerationRecipe:
        """Return a registered recipe."""

        try:
            return self._recipes[name]
        except KeyError as error:
            raise ValueError(
                f"Recipe '{name}' not found.",
            ) from error

    def list(
        self,
    ) -> tuple[GenerationRecipe, ...]:
        """Return all registered recipes."""

        return tuple(
            self._recipes.values(),
        )
