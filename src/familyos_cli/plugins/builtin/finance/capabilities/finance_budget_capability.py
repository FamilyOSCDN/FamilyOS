"""Finance budget capability."""

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class FinanceBudgetCapability:
    """Capability for finance budgets."""

    @staticmethod
    def create() -> PluginCapability:
        """Create budget capability."""

        return PluginCapability(
            id=PluginCapabilityId(
                "familyos.finance.budget",
            ),
            display_name="Finance Budget",
            description=(
                "Provides family financial budget management."
            ),
            metadata={
                "domain": "finance",
                "version": "1.0.0",
            },
        )
