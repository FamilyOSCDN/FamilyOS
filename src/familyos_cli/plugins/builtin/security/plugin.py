"""Built-in security plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.security.recipes.security_documentation_recipe import (
    SecurityDocumentationRecipe,
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


class SecurityPlugin(Plugin):
    """Built-in security generation plugin."""

    metadata = PluginMetadata(
        name="Security Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description="Generates security documentation.",
    )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return contributions exposed by the plugin."""

        return (
            GenerationContribution(
                preset=GenerationPresetId(
                    "security",
                ),
                description=(
                    "Security documentation package."
                ),
                recipes=(
                    "security_documentation",
                ),
            ),
            GenerationRecipeContribution(
                recipe=SecurityDocumentationRecipe(),
            ),
            TemplateContribution(
                template_directory=(
                    Path(__file__).parent
                    / "templates"
                    / "security"
                ),
            ),
        )
