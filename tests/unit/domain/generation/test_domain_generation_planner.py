from __future__ import annotations

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
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
from familyos_cli.domain.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
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

    assert [
        artifact.target_path
        for artifact in plan.artifacts
    ] == [
        "models/person.py",
        "aggregates/person.py",
        "repositories/person_repository.py",
        "services/person_registration_service.py",
    ]

    assert [
        artifact.template
        for artifact in plan.artifacts
    ] == [
        "entity.py.jinja",
        "aggregate.py.jinja",
        "repository.py.jinja",
        "service.py.jinja",
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
        aggregates=[],
        repositories=[],
        services=[],
    )

    planner = DomainGenerationPlanner(
        path_policy=FakeArtifactPathPolicy(),
    )

    plan = planner.create_plan(
        specification,
    )

    assert len(plan.artifacts) == 1

    assert plan.artifacts[0].target_path == (
        "custom/entity/Person.generated"
    )

    assert plan.artifacts[0].template == (
        "entity.py.jinja"
    )


def test_domain_generation_planner_creates_plan_from_recipe_request() -> None:
    registry = GenerationRecipeRegistry()

    registry.register(
        DomainDocumentationRecipe(),
    )

    planner = DomainGenerationPlanner(
        recipe_executor=RecipeExecutor(
            registry,
        ),
    )

    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    plan = planner.create_plan_from_request(
        request,
    )

    assert plan.domain_name == "Person"

    assert len(plan.artifacts) == 4

    assert plan.artifacts[0].kind == (
        ArtifactKind.DOCUMENTATION
    )

    assert plan.artifacts[0].target_path == (
        "docs/30-domains/person/README.md"
    )

    assert plan.artifacts[0].template == (
        "domain/README.md.j2"
    )
