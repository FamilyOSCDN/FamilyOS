"""Project initialization command."""

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.shared.exceptions import FamilyOSError


def init(name: str) -> None:
    """Initialize a new FamilyOS project."""

    try:
        use_case = CreateProjectUseCase()
        use_case.execute(name)

        Output.success(
            f'Project "{name}" created successfully.'
        )

    except FamilyOSError as error:
        Output.error(str(error))