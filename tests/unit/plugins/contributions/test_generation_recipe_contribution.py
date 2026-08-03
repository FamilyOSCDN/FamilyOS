"""Tests for generation recipe contribution."""

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


def test_generation_recipe_contribution_stores_recipe() -> None:
    """Contribution should store provided recipe."""

    recipe = FakeRecipe()

    contribution = GenerationRecipeContribution(
        recipe=recipe,
    )

    assert contribution.recipe is recipe
