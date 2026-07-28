from pathlib import Path

from familyos_cli.application.generation.default_generation_strategy_registry import (
    DefaultGenerationStrategyRegistry,
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
from familyos_cli.domain.models.aggregate_descriptor import (
    AggregateDescriptor,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.models.entity_descriptor import (
    EntityDescriptor,
)
from familyos_cli.domain.models.repository_descriptor import (
    RepositoryDescriptor,
)
from familyos_cli.domain.models.service_descriptor import (
    ServiceDescriptor,
)
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)


class FakeGenerationEngine:
    """Fake generation engine for unit tests."""

    def __init__(self) -> None:
        self.generated = False

    def generate(
        self,
        destination: Path,
        specification: GenerationSpecification,
        context: dict[str, object],
    ) -> None:
        self.generated = True


def test_create_domain_use_case_creates_generation_specification() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(
                name="Person",
                description="Person entity",
            ),
        ],
        aggregates=[
            AggregateDescriptor(
                name="Person",
                root_entity="Person",
                description="Person aggregate",
            ),
        ],
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                aggregate="Person",
                description="Person repository",
            ),
        ],
        services=[
            ServiceDescriptor(
                name="PersonService",
                description="Person service",
            ),
        ],
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

    strategy_registry = (
        DefaultGenerationStrategyRegistry.create()
    )

    engine = FakeGenerationEngine()

    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        specification_mapper=GenerationSpecificationMapper(),
        engine=engine,
        strategy_registry=strategy_registry,
    )

    use_case = CreateDomainUseCase(
        pipeline=pipeline,
        get_specification=get_specification,
        request_factory=GenerationRequestFactory(),
    )

    result = use_case.execute(
        domain_name="Person",
        destination=Path("."),
    )

    assert result is not None
    assert len(result.artifacts) > 0
    assert engine.generated is True
