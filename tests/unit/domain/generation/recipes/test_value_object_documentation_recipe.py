from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.recipes.value_object_documentation_recipe import (
    ValueObjectDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_value_object_documentation_recipe_name() -> None:
    recipe = ValueObjectDocumentationRecipe()

    assert recipe.name == "value_object_documentation"


def test_value_object_documentation_recipe_builds_artifacts() -> None:
    recipe = ValueObjectDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert len(artifacts) == 4

    assert [
        artifact.kind
        for artifact in artifacts
    ] == [
        ArtifactKind.DOCUMENTATION,
        ArtifactKind.DOCUMENTATION,
        ArtifactKind.DOCUMENTATION,
        ArtifactKind.DOCUMENTATION,
    ]

    assert [
        artifact.target_path
        for artifact in artifacts
    ] == [
        "docs/30-domains/person/value_objects/README.md",
        "docs/30-domains/person/value_objects/Attributes.md",
        "docs/30-domains/person/value_objects/Responsibilities.md",
        "docs/30-domains/person/value_objects/Business-Rules.md",
    ]
