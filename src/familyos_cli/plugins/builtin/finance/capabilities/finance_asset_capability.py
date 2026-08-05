"""Finance asset capability."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class FinanceAssetCapability:
    """Capability for finance assets."""

    @staticmethod
    def create() -> PluginCapability:
        """Create asset capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.finance.asset",
            ),
            display_name="Finance Asset",
            description=(
                "Provides family financial asset management."
            ),
            metadata={
                "domain": "finance",
                "version": "1.0.0",
            },
        )
