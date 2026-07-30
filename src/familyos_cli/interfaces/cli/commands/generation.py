"""Generation commands."""

from __future__ import annotations

import typer

from familyos_cli.interfaces.cli.commands.generation_presets import (
    generation_presets,
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
