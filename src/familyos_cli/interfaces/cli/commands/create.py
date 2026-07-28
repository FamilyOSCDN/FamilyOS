"""Create commands."""

import typer

from familyos_cli.interfaces.cli.commands.create_command import (
    CreateCommand,
)
from familyos_cli.interfaces.cli.commands.create_domain import (
    create_domain,
)

create_app = typer.Typer(
    help="Create FamilyOS artifacts.",
)


@create_app.command()
def artifact(
    artifact_type: str = typer.Argument(
        ...,
        help="Artifact type.",
    ),
    name: str = typer.Argument(
        ...,
        help="Artifact name.",
    ),
) -> None:
    """Create an artifact."""

    CreateCommand().execute(
        artifact_type=artifact_type,
        name=name,
    )


create_app.command()(create_domain)
