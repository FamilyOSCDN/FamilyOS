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


def test_domain_generation_planner_creates_full_domain_plan() -> None:
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

    planner = DomainGenerationPlanner()

    plan = planner.create_plan(specification)

    assert plan.domain_name == "Person"

    assert len(plan.artifacts) == 4

    artifact_types = [
        artifact.artifact_type
        for artifact in plan.artifacts
    ]

    assert artifact_types == [
        "entity",
        "aggregate",
        "repository",
        "service",
    ]


def test_domain_generation_planner_creates_empty_plan() -> None:
    specification = DomainSpecification(
        name="Empty",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    planner = DomainGenerationPlanner()

    plan = planner.create_plan(specification)

    assert plan.domain_name == "Empty"
    assert plan.artifacts == []