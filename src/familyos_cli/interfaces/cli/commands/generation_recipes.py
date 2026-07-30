"""Generation recipes command."""

from __future__ import annotations

from familyos_cli.interfaces.cli.context import (
    CommandContext,
)
from familyos_cli.interfaces.cli.output import (
    Output,
)


def generation_recipes() -> None:
    """Display available generation recipes."""

    context = CommandContext()

    recipes = context.recipe_catalog.list_recipes()

    Output.info(
        "Available generation recipes:",
    )

    for recipe in recipes:
        Output.info(
            f"  - {recipe.name}",
        )
