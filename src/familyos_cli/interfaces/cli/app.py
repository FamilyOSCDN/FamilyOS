"""Main Typer application."""

import typer

from familyos_cli.interfaces.cli.commands.init import init
from familyos_cli.interfaces.cli.commands.version import version

app = typer.Typer(
    name="familyos",
    help="FamilyOS CLI",
    no_args_is_help=True,
)

app.command()(version)
app.command()(init)