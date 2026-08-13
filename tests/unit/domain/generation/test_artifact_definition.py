from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)


def _set_attribute(
    instance: object,
    name: str,
    value: Any,
) -> None:
    setattr(
        instance,
        name,
        value,
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
        template="entity.py.jinja",
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        _set_attribute(
            artifact,
            "name",
            "Family",
        )
