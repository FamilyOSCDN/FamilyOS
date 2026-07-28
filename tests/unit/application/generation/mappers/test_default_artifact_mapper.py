from __future__ import annotations

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.mappers.default_artifact_mapper import (
    DefaultArtifactMapper,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)


def test_default_artifact_mapper_creates_generation_artifact() -> None:
    artifact_definition = ArtifactDefinition(
        kind=ArtifactKind.ENTITY,
        name="Person",
        target_path="models/person.py",
        template="entity.py.jinja",
    )

    mapper = DefaultArtifactMapper()

    result = mapper.map(
        artifact_definition,
    )

    assert isinstance(
        result,
        GenerationArtifact,
    )

    assert result.template == "entity.py.jinja"

    assert result.destination == "models/person.py"

    assert result.context.variables == {}

    assert result.context.project is None

    assert result.context.destination is None

    assert result.options.overwrite is False

    assert result.options.encoding == "utf-8"
