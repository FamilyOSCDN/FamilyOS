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
            ),
        ],
        metadata={
            "version": "1.0",
        },
    )

    assert plan.domain_name == "Person"
    assert len(plan.artifacts) == 2
    assert plan.artifacts[0].name == "Person"
    assert plan.metadata["version"] == "1.0"


def test_domain_generation_plan_is_immutable() -> None:
    plan = DomainGenerationPlan(
        domain_name="Person",
    )

    try:
        plan.domain_name = "Family"
    except AttributeError:
        assert True
    else:
        raise AssertionError("Expected code path was not reached.")
