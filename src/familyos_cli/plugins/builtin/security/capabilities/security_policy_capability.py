"""Security policy capability."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class SecurityPolicyCapability:
    """Factory for the security policy capability."""

    @staticmethod
    def create() -> PluginCapability:
        """Create the security policy capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "security.policy",
            ),
            display_name="Security Policy",
            description=(
                "Provides security policy management capabilities "
                "for FamilyOS."
            ),
            metadata={
                "domain": "security",
                "version": "1.0.0",
            },
        )