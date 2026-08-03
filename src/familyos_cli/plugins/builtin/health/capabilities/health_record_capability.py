"""Health record capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class HealthRecordCapability:
    """Factory for health record capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create health record capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.health.record",
            ),
            display_name=(
                "Health Record"
            ),
            description=(
                "Provides health record management capability."
            ),
        )
