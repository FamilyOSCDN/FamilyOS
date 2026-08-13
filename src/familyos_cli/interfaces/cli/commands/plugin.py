"""Plugin commands."""

from __future__ import annotations

from typing import Annotated

import typer

from familyos_cli.interfaces.cli.commands.plugin_compliance import (
    compliance_app,
)
from familyos_cli.interfaces.cli.commands.plugin_resolve import (
    EXIT_SUCCESS,
    plugin_resolve,
)

plugin_app = typer.Typer(
    help="Plugin ecosystem commands.",
    no_args_is_help=True,
)

plugin_app.add_typer(
    compliance_app,
    name="compliance",
)


@plugin_app.command(
    name="resolve",
)
def resolve(
    dependencies: Annotated[
        list[str],
        typer.Argument(
            ...,
            help=(
                "Plugin dependencies, for example "
                "'familyos.documentation>=1.0.0'."
            ),
        ),
    ],
    repository_name: Annotated[
        str,
        typer.Option(
            "--repository-name",
            help="Plugin repository name.",
        ),
    ],
    repository_url: Annotated[
        str,
        typer.Option(
            "--repository-url",
            help="Plugin repository URL.",
        ),
    ],
    repository_type: Annotated[
        str,
        typer.Option(
            "--repository-type",
            help="Plugin repository type.",
        ),
    ],
) -> None:
    """Resolve plugin dependencies."""

    exit_code = plugin_resolve(
        dependencies=dependencies,
        repository_name=repository_name,
        repository_url=repository_url,
        repository_type=repository_type,
    )

    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(
            code=exit_code,
        )
