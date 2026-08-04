"""FamilyOS Documents Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.documents.capabilities import (
    DocumentArchiveCapability,
    DocumentCapability,
)
from familyos_cli.plugins.builtin.documents.recipes import (
    DocumentsDocumentationRecipe,
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


class DocumentsPlugin(Plugin):
    """Official FamilyOS documents plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Documents Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides document management "
            "and family digital archive "
            "capabilities for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return provided capabilities."""

        return (
            DocumentCapability.create(),
            DocumentArchiveCapability.create(),
        )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return plugin contributions."""

        return (
            GenerationContribution(
                preset=GenerationPresetId(
                    "documents",
                ),
                description=(
                    "Generates FamilyOS "
                    "Documents domain artifacts."
                ),
                recipes=(
                    "documents-documentation",
                ),
            ),
            GenerationRecipeContribution(
                recipe=DocumentsDocumentationRecipe(),
            ),
            TemplateContribution(
                template_directory=(
                    Path(__file__).parent
                    / "templates"
                ),
            ),
        )
