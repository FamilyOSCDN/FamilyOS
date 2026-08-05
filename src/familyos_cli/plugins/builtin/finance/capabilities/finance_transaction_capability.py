"""Finance transaction capability."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class FinanceTransactionCapability:
    """Capability for finance transactions."""

    @staticmethod
    def create() -> PluginCapability:
        """Create transaction capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.finance.transaction",
            ),
            display_name="Finance Transaction",
            description=(
                "Provides family financial transaction management."
            ),
            metadata={
                "domain": "finance",
                "version": "1.0.0",
            },
        )
