"""CLI error handling."""

import typer

from familyos_cli.interfaces.cli.output import Output
from familyos_cli.shared.exceptions import FamilyOSError


class ErrorHandler:
    """Handle CLI errors consistently."""

    @staticmethod
    def handle(error: FamilyOSError) -> None:
        """Display a domain error and terminate."""

        Output.error(str(error))
        raise typer.Exit(code=1) from None
