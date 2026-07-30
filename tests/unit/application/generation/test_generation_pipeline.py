"""Tests for GenerationPipeline."""

from pathlib import Path

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.application.generation.generation_pipeline import (
    GenerationPipeline,
)
from familyos_cli.domain.models.project import Project
from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_pipeline_should_generate_project(
    tmp_path: Path,
) -> None:
    """GenerationPipeline should generate a project."""

    project_name = "demo"

    context = GenerationContext(
        project=Project(
            name=project_name,
        ),
        destination=tmp_path,
        variables={
            "project_name": project_name,
        },
    )

    runtime = PluginRuntime()

    pipeline = GenerationPipeline(
        generator=ProjectGenerator(),
        runtime=runtime,
    )

    result = pipeline.run(
        context,
    )

    assert result.success
