"""Filesystem project generator."""

from familyos_cli.domain.models.project import Project


class ProjectGenerator:
    """Generate a FamilyOS project on the filesystem."""

    def generate(self, project: Project) -> None:
        """Generate the project."""
        print(f"Generating project '{project.name}'...")