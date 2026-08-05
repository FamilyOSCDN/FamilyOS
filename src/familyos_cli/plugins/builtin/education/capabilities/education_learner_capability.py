"""Education learner capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class EducationLearnerCapability:
    """Factory for the education learner capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create education learner capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.education.learner",
            ),
            display_name=(
                "Education Learner"
            ),
            description=(
                "Provides learner management "
                "capabilities for FamilyOS education."
            ),
        )
