"""Use case for creating a new FamilyOS project."""

import typer


class CreateProjectUseCase:
    """Create a new FamilyOS project."""

    def execute(self, name: str) -> None:
        """Execute the use case."""
        typer.echo(f"Initializing project: {name}")