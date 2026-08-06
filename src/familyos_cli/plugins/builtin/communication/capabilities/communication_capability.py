"""Communication capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class CommunicationCapability:
    """Factory for the communication capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create communication capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.communication.messaging",
            ),
            display_name=(
                "Communication"
            ),
            description=(
                "Provides communication management "
                "capabilities for FamilyOS."
            ),
            metadata={
                "domain": "communication",
                "version": "1.0.0",
            },
        )
