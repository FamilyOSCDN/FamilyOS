"""FamilyOS Security Plugin."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.builtin.security.capabilities import (
    SecurityPolicyCapability,
    SecurityValidationCapability,
)
from familyos_cli.plugins.builtin.security.recipes.security_documentation_recipe import (
    SecurityDocumentationRecipe,
)
from familyos_cli.plugins.builtin.security.validation.security_validator import (
    SecurityValidator,
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
from familyos_cli.plugins.plugin import (
    Plugin,
)


class SecurityPlugin(Plugin):
    """Official FamilyOS security plugin."""

    metadata = PluginMetadata(
        name="FamilyOS Security Plugin",
        version="1.0.0",
        author="FamilyOS Team",
        description=(
            "Provides security capabilities, policies, "
            "validation rules, and security-related "
            "contributions for FamilyOS."
        ),
    )

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return capabilities exposed by the plugin."""

        return (
            SecurityPolicyCapability.create(),
            SecurityValidationCapability.create(),
        )

    def validator(
        self,
    ) -> SecurityValidator:
        """Return security validator."""

        return SecurityValidator()

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
