from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.builtin.documents.recipes import (
    DocumentsDocumentationRecipe,
)


def test_documents_documentation_recipe_name() -> None:
    recipe = DocumentsDocumentationRecipe()

    assert recipe.name == (
        "documents-documentation"
    )


def test_documents_documentation_recipe_builds_artifacts() -> None:
    recipe = DocumentsDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Documents",
        ),
    )

    assert len(artifacts) == 2

    assert [
        artifact.name
        for artifact in artifacts
    ] == [
        "documents-domain-documentation",
        "documents-capability-documentation",
    ]


def test_documents_documentation_recipe_uses_documentation_kind() -> None:
    recipe = DocumentsDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Documents",
        ),
    )

    assert all(
        artifact.kind
        is ArtifactKind.DOCUMENTATION
        for artifact in artifacts
    )


def test_documents_documentation_recipe_declares_targets() -> None:
    recipe = DocumentsDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Documents",
        ),
    )

    assert [
        artifact.target_path
        for artifact in artifacts
    ] == [
        "docs/documents",
        "docs/documents/capabilities",
    ]


def test_documents_documentation_recipe_declares_templates() -> None:
    recipe = DocumentsDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Documents",
        ),
    )

    assert [
        artifact.template
        for artifact in artifacts
    ] == [
        "documentation/documents_documentation.md.j2",
        "capabilities/documents_capabilities.md.j2",
    ]
