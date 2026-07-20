"""Filesystem project generator."""

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

    def __init__(self) -> None:
        """Initialize the project generator."""
        self._filesystem = FileSystemService()
        self._specification_loader = SpecificationLoader()
        self._generation_engine = GenerationEngine()

    def generate(self, project: Project) -> None:
        """Generate the project."""

        project_path = Path(project.name)

        self._filesystem.create_directory(project_path)

        specification = self._specification_loader.load(
            Path("specifications/project.yaml"),
        )

        self._generation_engine.generate(
            destination=project_path,
            specification=specification,
            context={
                "project_name": project.name,
            },
        )

        print(f"Project created: {project.name}")