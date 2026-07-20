"""Base class for CLI commands."""

from familyos_cli.interfaces.cli.context import CommandContext


class BaseCommand:
    """Base class for all CLI commands."""

    def __init__(self) -> None:
        """Initialize the command."""

        self.context = CommandContext()