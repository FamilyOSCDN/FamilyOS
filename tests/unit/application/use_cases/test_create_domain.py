from familyos_cli.application.use_cases.create_domain import (
    CreateDomainUseCase,
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

    use_case = CreateDomainUseCase(
        planner=DomainGenerationPlanner(),
    )

    plan = use_case.execute(specification)

    assert plan.domain_name == "Person"
    assert len(plan.artifacts) == 4