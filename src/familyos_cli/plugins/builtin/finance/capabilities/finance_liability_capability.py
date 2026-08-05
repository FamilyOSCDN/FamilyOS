"""Finance liability capability."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class FinanceLiabilityCapability:
    """Capability for finance liabilities."""

    @staticmethod
    def create() -> PluginCapability:
        """Create liability capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.finance.liability",
            ),
            display_name="Finance Liability",
            description=(
                "Provides family financial liability management."
            ),
            metadata={
                "domain": "finance",
                "version": "1.0.0",
            },
        )
