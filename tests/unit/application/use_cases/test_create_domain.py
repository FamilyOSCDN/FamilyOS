from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
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
from familyos_cli.domain.models.domain_specification import (
    AggregateDescriptor,
    DomainSpecification,
    EntityDescriptor,
    RepositoryDescriptor,
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
        specification: object,
        context: dict[str, str],
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

    engine = FakeGenerationEngine()

    pipeline = DomainGenerationPipeline(
        planner=DomainGenerationPlanner(),
        specification_mapper=GenerationSpecificationMapper(),
        engine=engine,
    )

    use_case = CreateDomainUseCase(
        pipeline=pipeline,
        get_specification=get_specification,
    )

    result = use_case.execute(
        domain_name="Person",
        destination=Path("."),
    )

    assert result is not None
    assert len(result.artifacts) > 0
    assert engine.generated is True
