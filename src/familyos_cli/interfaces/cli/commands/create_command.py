"""Create command."""

from familyos_cli.interfaces.cli.base_command import BaseCommand
from familyos_cli.interfaces.cli.error_handler import ErrorHandler
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.shared.exceptions import FamilyOSError


class CreateCommand(BaseCommand):
    """Create a FamilyOS artifact."""

    def execute(
        self,
        artifact_type: str,
        name: str,
    ) -> None:
        """Execute the command."""

        try:
            self.context.create_artifact.execute(
                artifact_type=artifact_type,
                name=name,
            )

            Output.success(
                f'{artifact_type.capitalize()} "{name}" created successfully.',
            )

        except FamilyOSError as error:
            ErrorHandler.handle(error)