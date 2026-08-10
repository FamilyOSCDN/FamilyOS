"""FamilyOS Education Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.education.capabilities import (
    EducationCourseCapability,
    EducationLearnerCapability,
    EducationRecordCapability,
)
from familyos_cli.plugins.builtin.education.recipes import (
    EducationDocumentationRecipe,
    EducationDomainRecipe,
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


class EducationPlugin(Plugin):
    """Official FamilyOS education plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Education Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides educational capabilities "
            "and family learning management "
            "support for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return provided capabilities."""

        return (
            EducationLearnerCapability.create(),
            EducationCourseCapability.create(),
            EducationRecordCapability.create(),
        )

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return plugin contributions."""

        return (
            GenerationContribution(
                id=PluginContributionId(
                    "familyos.education.generation",
                ),
                preset=GenerationPresetId(
                    "education",
                ),
                description=(
                    "Generates FamilyOS "
                    "education domain artifacts."
                ),
                recipes=(
                    "education-domain",
                    "education-documentation",
                ),
            ),
            GenerationRecipeContribution(
                id=PluginContributionId(
                    "familyos.education.recipe.domain",
                ),
                recipe=EducationDomainRecipe(),
            ),
            GenerationRecipeContribution(
                id=PluginContributionId(
                    "familyos.education.recipe.documentation",
                ),
                recipe=EducationDocumentationRecipe(),
            ),
            TemplateContribution(
                id=PluginContributionId(
                    "familyos.education.template",
                ),
                template_directory=(
                    Path(__file__).parent
                    / "templates"
                ),
            ),
        )
