from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import pytest

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.domain.models.project import (
    Project,
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


def test_generation_context_creation() -> None:
    project = Project(
        name="family-project",
    )

    context = GenerationContext(
        variables={
            "domain": "Person",
        },
        project=project,
        destination=Path(
            "generated/person.py",
        ),
    )

    assert context.variables == {
        "domain": "Person",
    }

    assert context.project == project

    assert context.destination == Path(
        "generated/person.py",
    )


def test_generation_context_defaults() -> None:
    context = GenerationContext()

    assert context.variables == {}

    assert context.project is None

    assert context.destination is None


def test_generation_context_is_immutable() -> None:
    context = GenerationContext()

    with pytest.raises(
        FrozenInstanceError,
    ):
        _set_attribute(
            context,
            "project",
            Project(
                name="new-project",
            ),
        )
