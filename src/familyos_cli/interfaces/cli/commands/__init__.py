"""Project initialization command."""

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


def init(name: str) -> None:
    """Initialize a new FamilyOS project."""
    use_case = CreateProjectUseCase()
    use_case.execute(name)