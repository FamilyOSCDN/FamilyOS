from __future__ import annotations

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)


def test_generation_specification_mapper_creates_specification() -> None:
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
    )

    mapper = GenerationSpecificationMapper()

    specification = mapper.map(plan)

    assert isinstance(
        specification,
        GenerationSpecification,
    )

    assert len(specification.artifacts) == 2

    assert (
        specification.artifacts[0].template
        == "entity.py.jinja"
    )

    assert (
        specification.artifacts[1].destination
        == "repositories/person_repository.py"
    )


def test_generation_specification_mapper_handles_empty_plan() -> None:
    plan = DomainGenerationPlan(
        domain_name="Empty",
    )

    mapper = GenerationSpecificationMapper()

    specification = mapper.map(plan)

    assert specification.artifacts == []
