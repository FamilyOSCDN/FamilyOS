"""Filesystem project generator."""

from pathlib import Path

from familyos_cli.domain.models.project import Project


class ProjectGenerator:
    """Generate a FamilyOS project on the filesystem."""

    def generate(self, project: Project) -> None:
        """Generate the project."""

        project_path = Path(project.name)

        project_path.mkdir(parents=True, exist_ok=False)

        print(f"Project created: {project.name}")