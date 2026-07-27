from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_generation_mapper import (
    ArtifactGenerationMapper,
)


def test_entity_artifact_gets_entity_template() -> None:
    artifact = ArtifactDefinition(
        artifact_type="entity",
        name="Person",
        target_path="domains/person/entities/person.py",
    )

    mapper = ArtifactGenerationMapper()

    result = mapper.map(artifact)

    assert result.template == "entity.py.jinja"