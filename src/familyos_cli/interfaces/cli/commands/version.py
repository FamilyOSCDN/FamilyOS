"""Version command."""

import typer


def version() -> None:
    """Display the FamilyOS CLI version."""
    typer.echo("FamilyOS CLI v0.1.0")