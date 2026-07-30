"""Generation presets command."""

from __future__ import annotations

from familyos_cli.interfaces.cli.context import (
    CommandContext,
)
from familyos_cli.interfaces.cli.output import (
    Output,
)


def generation_presets() -> None:
    """Display available generation presets."""

    context = CommandContext()

    catalog = (
        context.generation_catalog.get_catalog()
    )

    Output.info(
        "Available generation presets:",
    )

    for entry in catalog.list():
        Output.info(
            f"{entry.preset.value}",
        )

        Output.info(
            f"  {entry.description}",
        )

        Output.info(
            "  Recipes:",
        )

        for recipe in entry.recipes:
            Output.info(
                f"    - {recipe}",
            )
