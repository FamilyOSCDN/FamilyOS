"""Create command."""

import typer

from familyos_cli.interfaces.cli.commands.create_command import (
    CreateCommand,
)


def create(
    artifact_type: str = typer.Argument(
        ...,
        help="Artifact type (domain, aggregate, entity, module...).",
    ),
    name: str = typer.Argument(
        ...,
        help="Artifact name.",
    ),
) -> None:
    """Create a FamilyOS artifact."""

    CreateCommand().execute(
        artifact_type=artifact_type,
        name=name,
    )