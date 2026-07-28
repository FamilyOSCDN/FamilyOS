from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)


def test_domain_documentation_recipe_creates_documentation_artifacts() -> None:
    recipe = DomainDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        "Person",
    )

    assert recipe.name == "domain_documentation"

    assert recipe.profile == (
        GenerationProfile.DOMAIN_DOCUMENTATION
    )

    assert len(artifacts) == 4

    assert artifacts[0].kind == ArtifactKind.DOCUMENTATION

    assert artifacts[0].target_path == (
        "docs/30-domains/person/README.md"
    )

    assert artifacts[0].template == (
        "domain/README.md.j2"
    )
