"""Tests for plugin generation recipe contributor."""

from familyos_cli.application.generation.plugin_generation_recipe_contributor import (
    PluginGenerationRecipeContributor,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


class FakeRecipe:
    """Fake generation recipe."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "fake_recipe"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build fake artifacts."""

        _ = specification

        return []


def test_contributor_registers_plugin_recipe() -> None:
    """Contributor should register plugin recipes."""

    registry = GenerationRecipeRegistry()

    recipe = FakeRecipe()

    contribution = GenerationRecipeContribution(
        id=PluginContributionId(
            "familyos.test.recipe.fake",
        ),
        recipe=recipe,
    )

    PluginGenerationRecipeContributor().contribute(
        registry,
        (
            contribution,
        ),
    )

    assert registry.get(
        "fake_recipe",
    ) is recipe
