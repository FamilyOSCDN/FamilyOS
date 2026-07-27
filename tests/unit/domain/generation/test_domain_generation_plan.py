from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)


def test_domain_generation_plan_creation() -> None:
    plan = DomainGenerationPlan(
        domain_name="Person",
        artifacts=[
            ArtifactDefinition(
                artifact_type="entity",
                name="Person",
                target_path="models/person.py",
                template="entity.py.jinja",
            ),
            ArtifactDefinition(
                artifact_type="repository",
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
        assert False