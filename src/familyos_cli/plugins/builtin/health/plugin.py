"""FamilyOS Health Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.health.capabilities import (
    HealthProfileCapability,
    HealthRecordCapability,
)
from familyos_cli.plugins.builtin.health.recipes.health_documentation_recipe import (
    HealthDocumentationRecipe,
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
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)
from familyos_cli.plugins.models import PluginMetadata
from familyos_cli.plugins.plugin import Plugin


class HealthPlugin(Plugin):
    """Official FamilyOS health plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Health Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides health capabilities, health records, "
            "metrics, and validation support for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return capabilities exposed by the plugin."""

        return (
            HealthProfileCapability.create(),
            HealthRecordCapability.create(),
        )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return contributions exposed by the plugin."""

        return (
            GenerationContribution(
                id=PluginContributionId(
                    "familyos.health.generation",
                ),
                preset=GenerationPresetId(
                    "health",
                ),
                description=(
                    "Health documentation package."
                ),
                recipes=(
                    "health_documentation",
                ),
            ),
            GenerationRecipeContribution(
                id=PluginContributionId(
                    "familyos.health.recipe.documentation",
                ),
                recipe=HealthDocumentationRecipe(),
            ),
            TemplateContribution(
                id=PluginContributionId(
                    "familyos.health.template",
                ),
                template_directory=(
                    Path(__file__).parent
                    / "templates"
                    / "health"
                ),
            ),
        )
