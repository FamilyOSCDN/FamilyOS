"""Main Typer application."""

import typer

from familyos_cli.interfaces.cli.commands.create import create_app
from familyos_cli.interfaces.cli.commands.generation import (
    generation_app,
)
from familyos_cli.interfaces.cli.commands.init import init
from familyos_cli.interfaces.cli.commands.plugin import plugin_app
from familyos_cli.interfaces.cli.commands.version import version

app = typer.Typer(
    name="familyos",
    help="FamilyOS CLI",
    no_args_is_help=True,
)


app.add_typer(
    create_app,
    name="create",
)

app.add_typer(
    generation_app,
    name="generation",
)

app.add_typer(
    plugin_app,
    name="plugin",
)

app.command()(version)
app.command()(init)
