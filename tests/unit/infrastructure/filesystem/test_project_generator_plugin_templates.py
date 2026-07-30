"""Tests for ProjectGenerator."""

from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)


def test_should_expose_generation_engine() -> None:
    """ProjectGenerator should expose its generation engine."""

    generator = ProjectGenerator()

    assert generator.generation_engine is not None
