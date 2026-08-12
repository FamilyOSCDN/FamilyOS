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
    specification: Annotated[
        Path,
        typer.Option(
            "--specification",
            "-s",
            help="Path to the domain specification YAML file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
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
    recipe_name: Annotated[
        str | None,
        typer.Option(
            "--recipe",
            help="Generation recipe name.",
        ),
    ] = None,
    preset: Annotated[
        str | None,
        typer.Option(
            "--preset",
            help="Generation preset.",
        ),
    ] = None,
) -> None:
    """Create a FamilyOS domain."""

    context = CommandContext()

    target = destination or Path(".")

    try:
        loaded_specification = (
            context.domain_specification_loader.load(
                specification,
            )
        )

        if loaded_specification.name != name:
            Output.error(
                (
                    f'Domain specification name '
                    f'"{loaded_specification.name}" does not match '
                    f'requested domain "{name}".'
                ),
            )
            return

        result = context.create_domain.execute(
            domain_name=name,
            destination=target,
            recipe_name=recipe_name,
            preset=preset,
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
