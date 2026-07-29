from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.generation.recipes.domain_context_documentation_recipe import (
    DomainContextDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_domain_context_documentation_recipe_name() -> None:
    recipe = DomainContextDocumentationRecipe()

    assert recipe.name == "domain_context_documentation"


def test_domain_context_documentation_recipe_builds_artifacts() -> None:
    recipe = DomainContextDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
        business_rules=[
            "Person must have a unique identity",
        ],
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert recipe.profile == (
        GenerationProfile.DOMAIN_DOCUMENTATION
    )

    assert len(artifacts) == 5

    assert [
        artifact.kind
        for artifact in artifacts
    ] == [
        ArtifactKind.DOCUMENTATION,
    ] * 5

    assert [
        artifact.target_path
        for artifact in artifacts
    ] == [
        "docs/30-domains/person/Context.md",
        (
            "docs/30-domains/person/"
            "Responsibilities.md"
        ),
        (
            "docs/30-domains/person/"
            "Integrations.md"
        ),
        (
            "docs/30-domains/person/"
            "Business-Rules.md"
        ),
        (
            "docs/30-domains/person/"
            "diagrams/context-map.puml"
        ),
    ]

    assert [
        artifact.template
        for artifact in artifacts
    ] == [
        "domain_context/Context.md.j2",
        "domain_context/Responsibilities.md.j2",
        "domain_context/Integrations.md.j2",
        "domain_context/Business-Rules.md.j2",
        "domain_context/diagrams/context-map.puml.j2",
    ]
