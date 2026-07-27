"""Tests for GenerationContext."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.domain.models.project import Project


def test_generation_context_should_be_immutable() -> None:
    """GenerationContext should be immutable."""

    context = GenerationContext(
        project=Project(name="demo"),
        destination=Path("demo"),
        variables={
            "project_name": "demo",
        },
    )

    with pytest.raises(FrozenInstanceError):
        context.destination = Path("other")