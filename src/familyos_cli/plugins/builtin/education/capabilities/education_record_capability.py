"""Education record capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class EducationRecordCapability:
    """Factory for the education record capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create education record capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.education.record",
            ),
            display_name=(
                "Education Record"
            ),
            description=(
                "Provides educational record "
                "management capabilities for FamilyOS."
            ),
        )
