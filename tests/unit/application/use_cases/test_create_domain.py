from __future__ import annotations

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


def test_create_domain_use_case_creates_generation_plan() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(
                name="Person",
                description="Person entity",
            )
        ],
        aggregates=[
            AggregateDescriptor(
                name="Person",
                root_entity="Person",
                description="Person aggregate",
            )
        ],
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                aggregate="Person",
                description="Person repository",
            )
        ],
        services=[
            ServiceDescriptor(
                name="PersonService",
                description="Person service",
            )
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

    use_case = CreateDomainUseCase(
        planner=DomainGenerationPlanner(),
        get_specification=get_specification,
    )

    plan = use_case.execute(
        "Person",
    )

    assert plan is not None