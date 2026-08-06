"""Communication archive capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class CommunicationArchiveCapability:
    """Factory for the communication archive capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create communication archive capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.communication.archive",
            ),
            display_name=(
                "Communication Archive"
            ),
            description=(
                "Provides communication archive "
                "capabilities for FamilyOS."
            ),
            metadata={
                "domain": "communication",
                "version": "1.0.0",
            },
        )
