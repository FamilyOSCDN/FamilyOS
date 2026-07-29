from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_recipe_executor_creates_artifacts_from_request() -> None:
    registry = GenerationRecipeRegistry()

    registry.register(
        DomainDocumentationRecipe(),
    )

    executor = RecipeExecutor(
        registry,
    )

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    specification = DomainSpecification(
        name="Person",
    )

    artifacts = executor.execute(
        request,
        specification,
    )

    assert len(artifacts) == 4

    assert artifacts[0].target_path == (
        "docs/30-domains/person/README.md"
    )

    assert artifacts[0].template == (
        "domain/README.md.j2"
    )
