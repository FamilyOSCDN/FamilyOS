from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)


def test_domain_generation_plan_creation() -> None:
    plan = DomainGenerationPlan(
        domain_name="Person",
        artifacts=[
            ArtifactDefinition(
                kind=ArtifactKind.ENTITY,
                name="Person",
                target_path="models/person.py",
                template="entity.py.jinja",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.REPOSITORY,
                name="PersonRepository",
                target_path="repositories/person_repository.py",
                template="repository.py.jinja",
            ),
        ],
        metadata={
            "version": "1.0",
        },
    )

    assert plan.domain_name == "Person"
    assert len(plan.artifacts) == 2

    assert plan.artifacts[0].kind is ArtifactKind.ENTITY
    assert plan.artifacts[0].template == "entity.py.jinja"

    assert plan.artifacts[1].kind is ArtifactKind.REPOSITORY
    assert plan.artifacts[1].template == "repository.py.jinja"


def test_domain_generation_plan_defaults() -> None:
    plan = DomainGenerationPlan(
        domain_name="Empty",
    )

    assert plan.artifacts == []
    assert plan.metadata == {}
