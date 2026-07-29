from __future__ import annotations

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
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
from familyos_cli.domain.models.value_object_descriptor import (
    ValueObjectDescriptor,
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
                name="PersonRegistrationService",
                description="Person registration service",
            )
        ],
    )

    planner = DomainGenerationPlanner()

    plan = planner.create_plan(
        specification,
    )

    assert plan.domain_name == "Person"

    assert len(plan.artifacts) == 4

    assert [
        artifact.kind
        for artifact in plan.artifacts
    ] == [
        ArtifactKind.ENTITY,
        ArtifactKind.AGGREGATE,
        ArtifactKind.REPOSITORY,
        ArtifactKind.SERVICE,
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

    plan = planner.create_plan(
        specification,
    )

    assert plan.domain_name == "Empty"

    assert plan.artifacts == []


def test_domain_generation_planner_uses_injected_path_policy() -> None:
    class FakeArtifactPathPolicy:
        def path_for(
            self,
            kind: ArtifactKind,
            name: str,
        ) -> str:
            return f"custom/{kind.value}/{name}.generated"

    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(
                name="Person",
                description="Person entity",
            )
        ],
    )

    planner = DomainGenerationPlanner(
        path_policy=FakeArtifactPathPolicy(),
    )

    plan = planner.create_plan(
        specification,
    )

    assert plan.artifacts[0].target_path == (
        "custom/entity/Person.generated"
    )


def test_domain_generation_planner_creates_value_object_plan() -> None:
    specification = DomainSpecification(
        name="Person",
        value_objects=[
            ValueObjectDescriptor(
                name="EmailAddress",
                description="Email address value object",
            )
        ],
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    planner = DomainGenerationPlanner()

    plan = planner.create_plan(
        specification,
    )

    assert len(plan.artifacts) == 1

    assert plan.artifacts[0].kind == (
        ArtifactKind.VALUE_OBJECT
    )

    assert plan.artifacts[0].name == (
        "EmailAddress"
    )

    assert plan.artifacts[0].template == (
        "value_object.py.jinja"
    )

    assert plan.artifacts[0].target_path == (
        "value_objects/email_address.py"
    )
