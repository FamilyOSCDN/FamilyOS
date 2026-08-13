from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.builtin.health.recipes.health_documentation_recipe import (
    HealthDocumentationRecipe,
)


def test_health_documentation_recipe_metadata() -> None:
    """Recipe should expose metadata."""

    recipe = HealthDocumentationRecipe()

    assert recipe.name == "health_documentation"
    assert (
        recipe.profile
        == GenerationProfile.DOMAIN_DOCUMENTATION
    )


def test_health_documentation_recipe_builds_artifact() -> None:
    """Recipe should build health artifact."""

    recipe = HealthDocumentationRecipe()

    specification = DomainSpecification(
        name="Health",
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert len(artifacts) == 1

    artifact = artifacts[0]

    assert artifact.kind == ArtifactKind.DOCUMENTATION
    assert artifact.name == "Health"
    assert (
        artifact.target_path
        == "docs/30-domains/health/Health.md"
    )
    assert artifact.template == "Health.md.j2"
