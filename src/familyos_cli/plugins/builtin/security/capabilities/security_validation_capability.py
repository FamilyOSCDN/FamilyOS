"""Security validation capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class SecurityValidationCapability:
    """Factory for the security validation capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create the security validation capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.security.validation",
            ),
            display_name="Security Validation",
            description=(
                "Provides security validation capabilities "
                "for FamilyOS."
            ),
            metadata={
                "domain": "security",
                "version": "1.0.0",
            },
        )