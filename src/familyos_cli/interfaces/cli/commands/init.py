"""Init command."""

from familyos_cli.interfaces.cli.commands.init_command import InitCommand


def init(name: str) -> None:
    """Initialize a new FamilyOS project."""

    InitCommand().execute(name)
