"""Create domain command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.error_handler import ErrorHandler
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.shared.exceptions import FamilyOSError


def create_domain(
    name: Annotated[
        str,
        typer.Argument(
            ...,
            help="Domain name.",
        ),
    ],
    destination: Annotated[
        Path | None,
        typer.Option(
            "--destination",
            "-d",
            help="Generation destination.",
        ),
    ] = None,
) -> None:
    """Create a FamilyOS domain."""

    context = CommandContext()

    target = destination or Path(".")

    try:
        result = context.create_domain.execute(
            domain_name=name,
            destination=target,
        )

        if result is None:
            Output.error(
                f'Domain specification "{name}" not found.',
            )
            return

        Output.success(
            f'Domain "{name}" created successfully.',
        )

    except FamilyOSError as error:
        ErrorHandler.handle(error)
