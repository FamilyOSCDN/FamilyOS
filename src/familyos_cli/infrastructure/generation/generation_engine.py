"""Generation engine."""

from __future__ import annotations

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

    def __init__(
        self,
        template_directories: tuple[Path, ...] = (
            Path("templates"),
        ),
    ) -> None:
        """Initialize the generation engine."""
        self._directory_generator = DirectoryGenerator()
        self._file_generator = FileGenerator()

        self._template_directories = template_directories

    @property
    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return the template directories."""
        return self._template_directories

    def generate(
        self,
        destination: Path,
        specification: ProjectSpecification,
        context: dict[str, object],
    ) -> None:
        """Generate a project."""

        self._directory_generator.generate(
            destination=destination,
            directories=specification.directories,
        )

        self._file_generator.generate(
            destination=destination,
            files=specification.files,
            context=context,
        )