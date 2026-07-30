"""Generation domains command."""

from __future__ import annotations

from familyos_cli.interfaces.cli.context import (
    CommandContext,
)
from familyos_cli.interfaces.cli.output import (
    Output,
)


def generation_domains() -> None:
    """Display available domain generation contributions."""

    context = CommandContext()

    contributions = (
        context.domain_generation_catalog.list_domains()
    )

    Output.info(
        "Available generation domains:",
    )

    for contribution in contributions:
        Output.info(
            f"{contribution.domain}",
        )

        Output.info(
            f"  {contribution.description}",
        )

        Output.info(
            "  Artifacts:",
        )

        for artifact in contribution.artifacts:
            Output.info(
                f"    - {artifact}",
            )
