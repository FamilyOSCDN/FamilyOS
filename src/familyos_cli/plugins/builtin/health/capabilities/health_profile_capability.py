"""Health profile capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class HealthProfileCapability:
    """Factory for health profile capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create health profile capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.health.profile",
            ),
            display_name=(
                "Health Profile"
            ),
            description=(
                "Provides health profile management capability."
            ),
        )
