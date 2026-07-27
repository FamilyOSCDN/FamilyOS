from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)


def test_artifact_definition_creation() -> None:
    artifact = ArtifactDefinition(
        artifact_type="entity",
        name="Person",
        target_path="models/person.py",
        template="entity.py.jinja",
    )

    assert artifact.artifact_type == "entity"
    assert artifact.name == "Person"
    assert artifact.target_path == "models/person.py"
    assert artifact.template == "entity.py.jinja"


def test_artifact_definition_is_immutable() -> None:
    artifact = ArtifactDefinition(
        artifact_type="entity",
        name="Person",
        target_path="models/person.py",
    )

    try:
        artifact.name = "Family"
    except AttributeError:
        assert True
    else:
        assert False