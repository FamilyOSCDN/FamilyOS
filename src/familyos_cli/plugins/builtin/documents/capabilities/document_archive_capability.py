"""Document archive capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class DocumentArchiveCapability:
    """Factory for the document archive capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create document archive capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.documents.archive",
            ),
            display_name=(
                "Documents Archive"
            ),
            description=(
                "Provides family digital archive "
                "capabilities for FamilyOS documents."
            ),
            metadata={
                "domain": "documents",
                "version": "1.0.0",
            },
        )
