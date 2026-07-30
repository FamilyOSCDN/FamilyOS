"""Generation commands."""

from __future__ import annotations

import typer

from familyos_cli.interfaces.cli.commands.generation_domains import (
    generation_domains,
)
from familyos_cli.interfaces.cli.commands.generation_presets import (
    generation_presets,
)
from familyos_cli.interfaces.cli.commands.generation_recipes import (
    generation_recipes,
)

generation_app = typer.Typer(
    help="Generation discovery commands.",
)


@generation_app.command(
    name="presets",
)
def presets() -> None:
    """List available generation presets."""

    generation_presets()


@generation_app.command(
    name="domains",
)
def domains() -> None:
    """List available generation domains."""

    generation_domains()


@generation_app.command(
    name="recipes",
)
def recipes() -> None:
    """List available generation recipes."""

    generation_recipes()
