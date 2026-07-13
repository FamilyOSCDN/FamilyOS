"""Create project use case."""

from familyos_cli.domain.models.project import Project
from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)


class CreateProjectUseCase:
    """Create a new FamilyOS project."""

    def __init__(self) -> None:
        self.generator = ProjectGenerator()

    def execute(self, name: str) -> None:
        """Execute the use case."""
        project = Project(name=name)
        self.generator.generate(project)