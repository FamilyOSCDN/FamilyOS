"""Project specification model."""

from dataclasses import dataclass

from familyos_cli.domain.models.project_file import ProjectFile


@dataclass(frozen=True)
class ProjectSpecification:
    """Describe a FamilyOS project specification."""

    directories: list[str]
    files: list[ProjectFile]