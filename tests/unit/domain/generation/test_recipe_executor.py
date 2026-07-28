from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)


def test_recipe_executor_executes_registered_recipe() -> None:
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

    artifacts = executor.execute(
        request,
    )

    assert len(artifacts) == 4

    assert artifacts[0].kind == (
        ArtifactKind.DOCUMENTATION
    )

    assert artifacts[0].target_path == (
        "docs/30-domains/person/README.md"
    )
