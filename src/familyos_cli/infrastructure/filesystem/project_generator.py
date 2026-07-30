"""Filesystem project generator."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.project import Project
from familyos_cli.infrastructure.filesystem.file_system_service import (
    FileSystemService,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.infrastructure.specifications.specification_loader import (
    SpecificationLoader,
)


class ProjectGenerator:
    """Generate a FamilyOS project on the filesystem."""

    def __init__(
        self,
    ) -> None:
        """Initialize the project generator."""

        self._filesystem = FileSystemService()
        self._specification_loader = SpecificationLoader()
        self._generation_engine = GenerationEngine()

    @property
    def generation_engine(
        self,
    ) -> GenerationEngine:
        """Return the generation engine."""

        return self._generation_engine

    def generate(
        self,
        project: Project,
        destination: Path,
    ) -> None:
        """Generate the project."""

        project_path = destination / project.name

        self._filesystem.create_directory(
            project_path,
        )

        specification_path = (
            Path(__file__).resolve().parents[4]
            / "specifications"
            / "project.yaml"
        )

        specification = self._specification_loader.load(
            specification_path,
        )

        self._generation_engine.generate(
            destination=project_path,
            specification=specification,
            context={
                "project_name": project.name,
            },
        )
