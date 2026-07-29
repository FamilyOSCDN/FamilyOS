from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)


def test_default_recipe_registry_creates_registry() -> None:
    registry = DefaultRecipeRegistry.create()

    recipes = registry.list()

    assert len(recipes) == 2

    assert [
        recipe.name
        for recipe in recipes
    ] == [
        "domain_documentation",
        "value_object_documentation",
    ]
