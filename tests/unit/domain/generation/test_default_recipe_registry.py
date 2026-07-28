from familyos_cli.domain.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)


def test_default_recipe_registry_contains_domain_documentation_recipe() -> None:
    registry = DefaultRecipeRegistry.create()

    recipe = registry.get(
        "domain_documentation",
    )

    assert recipe.name == (
        "domain_documentation"
    )
