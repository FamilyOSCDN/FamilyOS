"""CLI command context."""

from __future__ import annotations

from functools import cached_property

from familyos_cli.application.use_cases.create_artifact import (
    CreateArtifactUseCase,
)
from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)
from familyos_cli.infrastructure.generation.artifact_generator import (
    ArtifactGenerator,
)


class CommandContext:
    """Shared context for CLI commands."""

    @cached_property
    def create_project(self) -> CreateProjectUseCase:
        """Provide project creation use case."""
        return CreateProjectUseCase()

    @cached_property
    def create_artifact(self) -> CreateArtifactUseCase:
        """Provide artifact creation use case."""
        return CreateArtifactUseCase(
            generator=ArtifactGenerator(),
        )