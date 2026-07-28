from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.domain.models.project import (
    Project,
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

    try:
        context.project = Project(
            name="new-project",
        )
    except AttributeError:
        assert True
    else:
        raise AssertionError(
            "Expected code path was not reached.",
        )
