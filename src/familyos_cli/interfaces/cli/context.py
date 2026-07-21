"""CLI command context."""

from familyos_cli.application.use_cases.create_artifact import (
    CreateArtifactUseCase,
)
from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


class CommandContext:
    """Provide shared services for CLI commands."""

    def __init__(self) -> None:
        """Initialize the CLI context."""

        self.create_project = CreateProjectUseCase()
        self.create_artifact = CreateArtifactUseCase()