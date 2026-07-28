from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)
from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
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
from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.application.use_cases.create_domain import (
    CreateDomainUseCase,
)
from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
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
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
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


class SpyGenerationRequestFactory(
    GenerationRequestFactory,
):
    """Track generated requests."""

    def __init__(self) -> None:
        self.request: GenerationRequest | None = None

    def create(
        self,
        domain_name: str,
        recipe_name: str = "domain_documentation",
    ) -> GenerationRequest:
        self.request = super().create(
            domain_name,
            recipe_name,
        )

        return self.request


def test_create_domain_use_case_creates_generation_request() -> None:
    specification = DomainSpecification(
        name="Person",
    )

    registry = DomainSpecificationRegistry()

    registry.register(
        specification,
    )

    specification_service = SpecificationService(
        registry,
    )

    get_specification = GetDomainSpecificationUseCase(
        specification_service,
    )

    recipe_executor = RecipeExecutor(
        DefaultRecipeRegistry.create(),
    )

    engine = FakeGenerationEngine()

    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        specification_mapper=GenerationSpecificationMapper(),
        engine=engine,
        recipe_executor=recipe_executor,
    )

    request_factory = SpyGenerationRequestFactory()

    use_case = CreateDomainUseCase(
        pipeline=pipeline,
        get_specification=get_specification,
        request_factory=request_factory,
    )

    result = use_case.execute(
        domain_name="Person",
        destination=Path("."),
    )

    assert result is not None

    assert request_factory.request is not None

    assert request_factory.request.domain_name == "Person"

    assert request_factory.request.recipe_name == (
        "domain_documentation"
    )
