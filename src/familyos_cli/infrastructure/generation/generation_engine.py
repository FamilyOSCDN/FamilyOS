"""Generation engine."""

from pathlib import Path

from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)
from familyos_cli.infrastructure.generation.directory_generator import (
    DirectoryGenerator,
)
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)


class GenerationEngine:
    """Generate a project from a specification."""

    def __init__(self) -> None:
        """Initialize the generation engine."""
        self._directory_generator = DirectoryGenerator()
        self._file_generator = FileGenerator()

    def generate(
        self,
        destination: Path,
        specification: ProjectSpecification,
        context: dict[str, object],
    ) -> None:
        """Generate a project."""

        self._directory_generator.generate(
            destination,
            specification.directories,
        )

        self._file_generator.generate(
            destination,
            specification.files,
            context,
        )