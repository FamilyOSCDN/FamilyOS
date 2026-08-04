"""FamilyOS Documents Plugin."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin import Plugin


class DocumentsPlugin(Plugin):
    """Official FamilyOS documents plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Documents Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides document management "
            "and family digital archive "
            "capabilities for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return provided capabilities."""

        return ()

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return plugin contributions."""

        return ()
