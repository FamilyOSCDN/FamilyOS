"""Create project use case."""

from __future__ import annotations

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


class CreateProjectUseCase:
    """Create a new FamilyOS project."""

    def __init__(
        self,
        pipeline: GenerationPipeline | None = None,
        runtime: PluginRuntime | None = None,
    ) -> None:
        """Initialize the use case."""

        if pipeline is not None:
            self._pipeline = pipeline
            return

        if runtime is None:
            runtime = PluginRuntime()

        self._pipeline = GenerationPipeline(
            generator=ProjectGenerator(),
            runtime=runtime,
        )

    def execute(
        self,
        name: str,
        destination: Path = Path("."),
    ) -> None:
        """Execute the use case."""

        self._pipeline.run(
            GenerationContext(
                project=Project(
                    name=name,
                ),
                destination=destination,
                variables={
                    "project_name": name,
                },
            ),
        )
