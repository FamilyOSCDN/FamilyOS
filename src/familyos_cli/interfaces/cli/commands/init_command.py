"""Project initialization command."""

from familyos_cli.interfaces.cli.base_command import BaseCommand
from familyos_cli.interfaces.cli.error_handler import ErrorHandler
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.shared.exceptions import FamilyOSError


class InitCommand(BaseCommand):
    """Initialize a new FamilyOS project."""

    def execute(self, name: str) -> None:
        """Execute the command."""

        try:
            self.context.create_project.execute(name)

            Output.success(
                f'Project "{name}" created successfully.',
            )

        except FamilyOSError as error:
            ErrorHandler.handle(error)
