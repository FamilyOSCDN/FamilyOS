"""Generation pipeline."""

from __future__ import annotations

from time import perf_counter

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.application.generation.generation_result import (
    GenerationResult,
)
from familyos_cli.application.ports.generation.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)


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

        if context.project is None:
            raise ValueError(
                "Generation project is required.",
            )

        if context.destination is None:
            raise ValueError(
                "Generation destination is required.",
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
