from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)
from familyos_cli.application.generation.generation_strategy_registry import (
    GenerationStrategyRegistry,
)
from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.application.generation.strategies.domain_documentation_strategy import (
    DomainDocumentationStrategy,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


def test_generation_strategy_registry_registers_strategy() -> None:
    registry = GenerationStrategyRegistry()

    strategy = DomainDocumentationStrategy(
        RecipeExecutor(
            DefaultRecipeRegistry.create(),
        ),
    )

    registry.register(
        strategy,
    )

    assert len(registry.list()) == 1


def test_generation_strategy_registry_resolves_strategy() -> None:
    registry = GenerationStrategyRegistry()

    strategy = DomainDocumentationStrategy(
        RecipeExecutor(
            DefaultRecipeRegistry.create(),
        ),
    )

    registry.register(
        strategy,
    )

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    resolved = registry.resolve(
        request,
    )

    assert resolved.name == (
        "domain_documentation"
    )


def test_generation_strategy_registry_fails_when_missing() -> None:
    registry = GenerationStrategyRegistry()

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="unknown",
    )

    try:
        registry.resolve(
            request,
        )
    except ValueError as error:
        assert "No strategy found" in str(error)
    else:
        raise AssertionError(
            "Expected ValueError",
        )
