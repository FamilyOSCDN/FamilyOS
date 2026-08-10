"""Security plugin contributions."""

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
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)
from familyos_cli.plugins.contributions.template_contribution import (
    TemplateContribution,
)

SECURITY_GENERATION_CONTRIBUTION = GenerationContribution(
    id=PluginContributionId(
        "familyos.security.generation",
    ),
    preset=GenerationPresetId(
        "security",
    ),
    description="Generate security-related artifacts.",
    recipes=(
        "security_documentation",
    ),
)


SECURITY_DOCUMENTATION_RECIPE_CONTRIBUTION = (
    GenerationRecipeContribution(
        id=PluginContributionId(
            "familyos.security.recipe.documentation",
        ),
        recipe=SecurityDocumentationRecipe(),
    )
)


SECURITY_TEMPLATE_CONTRIBUTION = TemplateContribution(
    id=PluginContributionId(
        "familyos.security.template",
    ),
    template_directory=Path(
        "src/familyos_cli/plugins/builtin/security/templates/security",
    ),
)


SECURITY_CONTRIBUTIONS: tuple[Contribution, ...] = (
    SECURITY_GENERATION_CONTRIBUTION,
    SECURITY_DOCUMENTATION_RECIPE_CONTRIBUTION,
    SECURITY_TEMPLATE_CONTRIBUTION,
)
