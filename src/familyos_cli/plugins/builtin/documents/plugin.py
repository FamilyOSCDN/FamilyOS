"""FamilyOS Documents Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
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

from .capabilities.document_archive_capability import (
    DocumentArchiveCapability,
)
from .capabilities.document_capability import (
    DocumentCapability,
)
from .recipes.documents_documentation_recipe import (
    DocumentsDocumentationRecipe,
)


class DocumentsPlugin(Plugin):
    """Official FamilyOS documents plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Documents Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides document management capabilities "
            "and family digital archive services for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return document capabilities."""

        return (
            DocumentCapability.create(),
            DocumentArchiveCapability.create(),
        )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return plugin contributions."""

        template_directory = (
            Path(__file__).parent / "templates"
        )

        return (
            GenerationContribution(
                id=PluginContributionId(
                    "familyos.documents.generation",
                ),
                preset=GenerationPresetId(
                    "documents",
                ),
                description=(
                    "Generate FamilyOS documents "
                    "domain artifacts."
                ),
                recipes=(
                    "documents-documentation",
                ),
            ),
            GenerationRecipeContribution(
                id=PluginContributionId(
                    "familyos.documents.recipe.documentation",
                ),
                recipe=DocumentsDocumentationRecipe(),
            ),
            TemplateContribution(
                id=PluginContributionId(
                    "familyos.documents.template",
                ),
                template_directory=template_directory,
            ),
        )
