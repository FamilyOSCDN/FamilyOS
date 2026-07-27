"""Generation pipeline."""

from __future__ import annotations

from time import perf_counter

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.application.generation.generation_result import (
    GenerationResult,
)
from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class GenerationPipeline:
    """Coordinate the project generation pipeline."""

    def __init__(
        self,
        generator: ProjectGenerator,
        runtime: PluginRuntime,
    ) -> None:
        """Initialize the generation pipeline."""
        self._generator = generator
        self._runtime = runtime

    def run(
        self,
        context: GenerationContext,
    ) -> GenerationResult:
        """Execute the generation pipeline."""

        start = perf_counter()

        self._runtime.before_generate(
            context,
        )

        self._generator.generate(
            project=context.project,
            destination=context.destination,
        )

        self._runtime.after_generate(
            context,
        )

        duration = perf_counter() - start

        return GenerationResult(
            success=True,
            generated_files=(),
            warnings=(),
            duration=duration,
        )