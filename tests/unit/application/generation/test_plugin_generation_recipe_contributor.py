"""Tests for plugin generation recipe contributor."""

from familyos_cli.application.generation.plugin_generation_recipe_contributor import (
    PluginGenerationRecipeContributor,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.plugins.contributions.generation_recipe_contribution import (
    GenerationRecipeContribution,
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
        specification,
    ):
        """Build fake artifacts."""

        return []


def test_contributor_registers_plugin_recipe() -> None:
    """Contributor should register plugin recipes."""

    registry = GenerationRecipeRegistry()

    recipe = FakeRecipe()

    contribution = GenerationRecipeContribution(
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
