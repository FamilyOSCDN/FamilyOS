"""Finance account capability."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class FinanceAccountCapability:
    """Capability for finance accounts."""

    @staticmethod
    def create() -> PluginCapability:
        """Create account capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.finance.account",
            ),
            display_name="Finance Account",
            description=(
                "Provides family financial account management."
            ),
            metadata={
                "domain": "finance",
                "version": "1.0.0",
            },
        )
