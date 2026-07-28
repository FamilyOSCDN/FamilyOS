"""Base class for CLI commands."""

from familyos_cli.interfaces.cli.context import (
    CommandContext,
)


class BaseCommand:
    """Base class for all CLI commands."""

    def __init__(
        self,
        context: CommandContext | None = None,
    ) -> None:
        """Initialize command."""

        self.context = context if context is not None else CommandContext()
