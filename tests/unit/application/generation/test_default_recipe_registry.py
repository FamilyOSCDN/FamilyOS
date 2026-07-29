from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)


def test_default_recipe_registry_creates_registry() -> None:
    registry = DefaultRecipeRegistry.create()

    recipes = registry.list()

    assert len(recipes) == 8

    assert [
        recipe.name
        for recipe in recipes
    ] == [
        "domain_documentation",
        "entity_documentation",
        "value_object_documentation",
        "aggregate_documentation",
        "domain_context_documentation",
        "repository_documentation",
        "service_documentation",
        "full_domain_documentation",
    ]
