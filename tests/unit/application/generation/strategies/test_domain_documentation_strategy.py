from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
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
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_domain_documentation_strategy_name() -> None:
    strategy = DomainDocumentationStrategy(
        RecipeExecutor(
            DefaultRecipeRegistry.create(),
        ),
    )

    assert strategy.name == "domain_documentation"


def test_domain_documentation_strategy_supports_request() -> None:
    strategy = DomainDocumentationStrategy(
        RecipeExecutor(
            DefaultRecipeRegistry.create(),
        ),
    )

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    assert strategy.supports(
        request,
    )


def test_domain_documentation_strategy_generates_plan() -> None:
    strategy = DomainDocumentationStrategy(
        RecipeExecutor(
            DefaultRecipeRegistry.create(),
        ),
    )

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    specification = DomainSpecification(
        name="Person",
    )

    plan = strategy.execute(
        request,
        specification,
    )

    assert plan.domain_name == "Person"

    assert len(plan.artifacts) == 4

    assert plan.metadata["strategy"] == (
        "domain_documentation"
    )
