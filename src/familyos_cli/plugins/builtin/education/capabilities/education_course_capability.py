"""Education course capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class EducationCourseCapability:
    """Factory for the education course capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create education course capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.education.course",
            ),
            display_name=(
                "Education Course"
            ),
            description=(
                "Provides course management "
                "capabilities for FamilyOS education."
            ),
        )
