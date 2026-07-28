"""Tests for ProjectGenerator plugin templates."""

from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_should_expose_generation_engine() -> None:
    """ProjectGenerator should expose its generation engine."""

    runtime = PluginRuntime()

    generator = ProjectGenerator(
        runtime=runtime,
    )

    assert generator.generation_engine is not None
