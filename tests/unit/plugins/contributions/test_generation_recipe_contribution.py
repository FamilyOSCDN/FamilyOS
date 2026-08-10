"""Tests for generation recipe contribution."""

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
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
    """Recipe used by contribution tests."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "fake"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Return no artifacts."""

        _ = specification

        return []


def test_generation_recipe_contribution_stores_recipe() -> None:
    """Contribution should store provided recipe."""

    recipe = FakeRecipe()

    contribution = GenerationRecipeContribution(
        id=PluginContributionId(
            "familyos.test.recipe.fake",
        ),
        recipe=recipe,
    )

    assert contribution.id == PluginContributionId(
        "familyos.test.recipe.fake",
    )

    assert contribution.recipe is recipe
