from typing import assert_type

from familyos_cli.application.generation.mappers.artifact_mapper import (
    ArtifactMapper,
)


def test_artifact_mapper_is_a_protocol() -> None:
    assert_type(
        ArtifactMapper,
        type[ArtifactMapper],
    )