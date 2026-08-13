from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.application.generation.generation_options import (
    GenerationOptions,
)
from familyos_cli.domain.models.project import Project


def test_generation_artifact_creation() -> None:
    project = Project(
        name="family-project",
    )

    destination = Path(
        "models/person.py",
    )

    artifact = GenerationArtifact(
        template="entity.py.jinja",
        destination="models/person.py",
        context=GenerationContext(
            variables={
                "name": "Person",
            },
            project=project,
            destination=destination,
        ),
        options=GenerationOptions(
            overwrite=True,
            encoding="utf-16",
        ),
    )

    assert artifact.template == "entity.py.jinja"

    assert artifact.destination == "models/person.py"

    assert artifact.context.variables == {
        "name": "Person",
    }

    assert artifact.context.project == project

    assert artifact.context.destination == destination

    assert artifact.options.overwrite is True

    assert artifact.options.encoding == "utf-16"


def test_generation_artifact_defaults() -> None:
    artifact = GenerationArtifact(
        template="readme.md.jinja",
        destination="README.md",
    )

    assert artifact.context.variables == {}

    assert artifact.context.project is None

    assert artifact.context.destination is None

    assert artifact.options.overwrite is False

    assert artifact.options.encoding == "utf-8"


def test_generation_artifact_custom_options() -> None:
    artifact = GenerationArtifact(
        template="entity.py.jinja",
        destination="models/person.py",
        options=GenerationOptions(
            overwrite=True,
            encoding="utf-16",
            create_directories=False,
            dry_run=True,
        ),
    )

    assert artifact.options.overwrite is True

    assert artifact.options.encoding == "utf-16"

    assert artifact.options.create_directories is False

    assert artifact.options.dry_run is True


def test_generation_artifact_is_immutable() -> None:
    artifact = GenerationArtifact(
        template="entity.py.jinja",
        destination="models/person.py",
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        artifact.__setattr__(
            "template",
            "service.py.jinja",
        )
