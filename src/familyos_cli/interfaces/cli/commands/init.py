"""Project initialization command."""

import typer


def init(name: str) -> None:
    """Initialize a new FamilyOS project."""
    typer.echo(f"Initializing project: {name}")