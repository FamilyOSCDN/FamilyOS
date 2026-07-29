from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.generation.recipes.entity_documentation_recipe import (
    EntityDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.models.entity_descriptor import (
    EntityDescriptor,
)


def test_entity_documentation_recipe_name() -> None:
    recipe = EntityDocumentationRecipe()

    assert recipe.name == "entity_documentation"


def test_entity_documentation_recipe_builds_artifacts() -> None:
    recipe = EntityDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(
                name="Person",
                description="Human identity entity",
            )
        ],
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert recipe.profile == (
        GenerationProfile.DOMAIN_DOCUMENTATION
    )

    assert len(artifacts) == 3

    assert [
        artifact.kind
        for artifact in artifacts
    ] == [
        ArtifactKind.DOCUMENTATION,
        ArtifactKind.DOCUMENTATION,
        ArtifactKind.DOCUMENTATION,
    ]

    assert [
        artifact.target_path
        for artifact in artifacts
    ] == [
        "docs/30-domains/person/entities/person/README.md",
        "docs/30-domains/person/entities/person/Attributes.md",
        "docs/30-domains/person/entities/person/Responsibilities.md",
    ]

    assert [
        artifact.template
        for artifact in artifacts
    ] == [
        "entity/README.md.j2",
        "entity/Attributes.md.j2",
        "entity/Responsibilities.md.j2",
    ]

    assert artifacts[0].context["entity"].name == (
        "Person"
    )
