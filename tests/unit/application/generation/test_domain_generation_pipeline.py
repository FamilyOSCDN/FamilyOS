from pathlib import Path

from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)
from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.generation_strategy_registry import (
    GenerationStrategyRegistry,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.application.generation.strategies.domain_documentation_strategy import (
    DomainDocumentationStrategy,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class FakeGenerationEngine:
    """Fake generation engine."""

    def __init__(self) -> None:
        self.generated = False

    def generate(
        self,
        destination: Path,
        specification: GenerationSpecification,
        context: dict[str, object],
    ) -> None:
        self.generated = True


def test_domain_generation_pipeline_creates_generation_specification() -> None:
    strategy_registry = GenerationStrategyRegistry()

    strategy_registry.register(
        DomainDocumentationStrategy(
            RecipeExecutor(
                DefaultRecipeRegistry.create(),
            ),
        ),
    )

    engine = FakeGenerationEngine()

    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        specification_mapper=GenerationSpecificationMapper(),
        engine=engine,
        strategy_registry=strategy_registry,
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

    assert engine.generated is True
