from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
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


def test_generation_specification_creation() -> None:
    specification = GenerationSpecification(
        directories=[
            "docs",
            "src",
        ],
        artifacts=[
            GenerationArtifact(
                template="entity.py.jinja",
                destination="models/person.py",
            ),
            GenerationArtifact(
                template="repository.py.jinja",
                destination="repositories/person_repository.py",
            ),
        ],
    )

    assert specification.directories == [
        "docs",
        "src",
    ]

    assert len(specification.artifacts) == 2

    assert specification.artifacts[0].template == (
        "entity.py.jinja"
    )

    assert specification.artifacts[1].destination == (
        "repositories/person_repository.py"
    )


def test_generation_specification_defaults() -> None:
    specification = GenerationSpecification()

    assert specification.directories == []

    assert specification.artifacts == []


def test_generation_specification_is_immutable() -> None:
    specification = GenerationSpecification()

    with pytest.raises(
        FrozenInstanceError,
    ):
        _set_attribute(
            specification,
            "artifacts",
            [],
        )
