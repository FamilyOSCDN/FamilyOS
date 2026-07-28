from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
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
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


def test_domain_generation_pipeline_creates_generation_specification() -> None:
    registry = GenerationRecipeRegistry()

    registry.register(
        DomainDocumentationRecipe(),
    )

    recipe_executor = RecipeExecutor(
        registry,
    )

    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        specification_mapper=GenerationSpecificationMapper(),
        engine=GenerationEngine(),
        recipe_executor=recipe_executor,
    )

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    specification = DomainSpecification(
        name="Person",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    result = pipeline.generate(
        request=request,
        specification=specification,
        destination=Path("generated"),
    )

    assert isinstance(
        result,
        GenerationSpecification,
    )

    assert len(result.artifacts) == 4
