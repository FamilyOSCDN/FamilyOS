from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)


def test_should_expose_expected_artifact_kinds() -> None:
    assert ArtifactKind.ENTITY.value == "entity"
    assert ArtifactKind.AGGREGATE.value == "aggregate"
    assert ArtifactKind.REPOSITORY.value == "repository"
    assert ArtifactKind.SERVICE.value == "service"
    assert ArtifactKind.VALUE_OBJECT.value == "value_object"