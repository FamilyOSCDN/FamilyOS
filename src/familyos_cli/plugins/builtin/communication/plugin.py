"""FamilyOS Communication Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.communication.capabilities import (
    CommunicationArchiveCapability,
    CommunicationCapability,
)
from familyos_cli.plugins.builtin.communication.recipes import (
    CommunicationDocumentationRecipe,
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


class CommunicationPlugin(Plugin):
    """Official FamilyOS communication plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Communication Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides communication management "
            "and communication archive capabilities "
            "for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return communication capabilities."""

        return (
            CommunicationCapability.create(),
            CommunicationArchiveCapability.create(),
        )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return plugin contributions."""

        template_directory = (
            Path(__file__).parent
            / "templates"
        )

        return (
            GenerationContribution(
                id=PluginContributionId(
                    "familyos.communication.generation",
                ),
                preset=GenerationPresetId(
                    "communication",
                ),
                description=(
                    "Generate FamilyOS communication "
                    "domain artifacts."
                ),
                recipes=(
                    "communication-documentation",
                ),
            ),
            GenerationRecipeContribution(
                id=PluginContributionId(
                    "familyos.communication.recipe.documentation",
                ),
                recipe=CommunicationDocumentationRecipe(),
            ),
            TemplateContribution(
                id=PluginContributionId(
                    "familyos.communication.template",
                ),
                template_directory=template_directory,
            ),
        )
