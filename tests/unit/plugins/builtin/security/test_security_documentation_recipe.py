from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.builtin.security.recipes.security_documentation_recipe import (
    SecurityDocumentationRecipe,
)


def test_security_documentation_recipe_metadata() -> None:
    """Recipe should expose metadata."""

    recipe = SecurityDocumentationRecipe()

    assert recipe.name == "security_documentation"
    assert (
        recipe.profile
        == GenerationProfile.DOMAIN_DOCUMENTATION
    )


def test_security_documentation_recipe_builds_artifact() -> None:
    """Recipe should build security artifact."""

    recipe = SecurityDocumentationRecipe()

    specification = DomainSpecification(
        name="Security",
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert len(artifacts) == 1

    artifact = artifacts[0]

    assert artifact.kind == ArtifactKind.DOCUMENTATION
    assert artifact.name == "Security"
    assert (
        artifact.target_path
        == "docs/30-domains/security/Security.md"
    )
    assert artifact.template == "Security.md.j2"
