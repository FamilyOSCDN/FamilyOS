"""Document capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class DocumentCapability:
    """Factory for the document capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create document capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.documents.document",
            ),
            display_name=(
                "Documents"
            ),
            description=(
                "Provides document management "
                "capabilities for FamilyOS."
            ),
            metadata={
                "domain": "documents",
                "version": "1.0.0",
            },
        )
