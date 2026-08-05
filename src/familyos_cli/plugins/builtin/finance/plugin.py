"""FamilyOS Finance Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.finance.capabilities.finance_account_capability import (
    FinanceAccountCapability,
)
from familyos_cli.plugins.builtin.finance.capabilities.finance_asset_capability import (
    FinanceAssetCapability,
)
from familyos_cli.plugins.builtin.finance.capabilities.finance_budget_capability import (
    FinanceBudgetCapability,
)
from familyos_cli.plugins.builtin.finance.capabilities.finance_liability_capability import (
    FinanceLiabilityCapability,
)
from familyos_cli.plugins.builtin.finance.capabilities.finance_transaction_capability import (
    FinanceTransactionCapability,
)
from familyos_cli.plugins.builtin.finance.recipes.finance_documentation_recipe import (
    FinanceDocumentationRecipe,
)
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin import Plugin


class FinancePlugin(Plugin):
    """Official FamilyOS finance plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Finance Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides financial capabilities, "
            "accounts, transactions, assets, "
            "liabilities, and budgets support "
            "for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return finance capabilities."""

        return (
            FinanceAccountCapability.create(),
            FinanceTransactionCapability.create(),
            FinanceAssetCapability.create(),
            FinanceLiabilityCapability.create(),
            FinanceBudgetCapability.create(),
        )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return finance contributions."""

        return (
            GenerationContribution(
                preset=GenerationPresetId(
                    "finance",
                ),
                description=(
                    "Generates finance domain artifacts."
                ),
                recipes=(
                    "finance_documentation",
                ),
            ),
            GenerationRecipeContribution(
                recipe=FinanceDocumentationRecipe(),
            ),
            TemplateContribution(
                template_directory=(
                    Path(__file__).parent
                    / "templates"
                    / "finance"
                ),
            ),
        )
