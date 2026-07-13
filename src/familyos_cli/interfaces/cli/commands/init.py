"""Init command."""

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


def init(name: str) -> None:
    """Initialize a new FamilyOS project."""
    CreateProjectUseCase().execute(name)