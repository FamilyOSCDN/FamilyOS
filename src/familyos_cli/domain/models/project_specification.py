"""Project specification model."""

from dataclasses import dataclass, field

from familyos_cli.domain.models.project_file import ProjectFile


@dataclass(slots=True, frozen=True)
class ProjectSpecification:
    """Describe everything needed to generate a project."""

    directories: list[str] = field(default_factory=list)
    files: list[ProjectFile] = field(default_factory=list)