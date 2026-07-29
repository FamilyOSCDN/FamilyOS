from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_domain_documentation_recipe_creates_documentation_artifacts() -> None:
    recipe = DomainDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
    )

    artifacts = recipe.build_artifacts(
        specification,
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
