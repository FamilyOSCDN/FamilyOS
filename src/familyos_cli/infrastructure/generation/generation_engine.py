"""Generation engine."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.infrastructure.generation.directory_generator import (
    DirectoryGenerator,
)
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)
from familyos_cli.infrastructure.generation.generation_specification_adapter import (
    GenerationSpecificationAdapter,
)


class GenerationEngine:
    """Generate artifacts from a generation specification."""

    def __init__(
        self,
        template_directories: tuple[Path, ...] = (
            Path("templates"),
        ),
    ) -> None:
        """Initialize the generation engine."""

        self._template_directories = template_directories

        self._directory_generator = DirectoryGenerator()

        self._file_generator = FileGenerator(
            template_directories=template_directories,
        )

        self._adapter = GenerationSpecificationAdapter()

    @property
    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return template directories."""

        return self._template_directories

    def generate(
        self,
        destination: Path,
        specification: GenerationSpecification,
        context: dict[str, object],
    ) -> None:
        """Generate artifacts."""

        project_specification = self._adapter.adapt(
            specification,
        )

        self._directory_generator.generate(
            destination=destination,
            directories=project_specification.directories,
        )

        self._file_generator.generate(
            destination=destination,
            files=project_specification.files,
            context=context,
        )
