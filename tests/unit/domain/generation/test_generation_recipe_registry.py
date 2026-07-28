from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)


def test_registry_registers_and_returns_recipe() -> None:
    registry = GenerationRecipeRegistry()

    recipe = DomainDocumentationRecipe()

    registry.register(
        recipe,
    )

    result = registry.get(
        "domain_documentation",
    )

    assert result.name == (
        "domain_documentation"
    )


def test_registry_lists_registered_recipes() -> None:
    registry = GenerationRecipeRegistry()

    registry.register(
        DomainDocumentationRecipe(),
    )

    recipes = registry.list()

    assert len(recipes) == 1

    assert recipes[0].name == (
        "domain_documentation"
    )


def test_registry_rejects_duplicate_recipe() -> None:
    registry = GenerationRecipeRegistry()

    registry.register(
        DomainDocumentationRecipe(),
    )

    try:
        registry.register(
            DomainDocumentationRecipe(),
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError.",
        )
