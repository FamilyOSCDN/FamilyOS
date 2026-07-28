from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)


def test_artifact_definition_creation() -> None:
    artifact = ArtifactDefinition(
        kind=ArtifactKind.ENTITY,
        name="Person",
        target_path="models/person.py",
        template="entity.py.jinja",
    )

    assert artifact.kind is ArtifactKind.ENTITY
    assert artifact.name == "Person"
    assert artifact.target_path == "models/person.py"
    assert artifact.template == "entity.py.jinja"


def test_artifact_definition_is_immutable() -> None:
    artifact = ArtifactDefinition(
        kind=ArtifactKind.ENTITY,
        name="Person",
        target_path="models/person.py",
    )

    try:
        artifact.name = "Family"
    except AttributeError:
        pass
    else:
        raise AssertionError("Expected AttributeError.")