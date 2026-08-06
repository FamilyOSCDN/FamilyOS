"""Tests for CommunicationDocumentationRecipe."""

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.builtin.communication.recipes import (
    CommunicationDocumentationRecipe,
)


def test_communication_documentation_recipe_name() -> None:
    recipe = CommunicationDocumentationRecipe()

    assert recipe.name == (
        "communication-documentation"
    )


def test_communication_documentation_recipe_builds_artifacts() -> None:
    recipe = CommunicationDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Communication",
        ),
    )

    assert len(artifacts) == 2

    assert [
        artifact.name
        for artifact in artifacts
    ] == [
        "communication-domain-documentation",
        "communication-capability-documentation",
    ]


def test_communication_documentation_recipe_uses_documentation_kind() -> None:
    recipe = CommunicationDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Communication",
        ),
    )

    assert all(
        artifact.kind
        is ArtifactKind.DOCUMENTATION
        for artifact in artifacts
    )


def test_communication_documentation_recipe_declares_targets() -> None:
    recipe = CommunicationDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Communication",
        ),
    )

    assert [
        artifact.target_path
        for artifact in artifacts
    ] == [
        "docs/communication",
        "docs/communication/capabilities",
    ]


def test_communication_documentation_recipe_declares_templates() -> None:
    recipe = CommunicationDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Communication",
        ),
    )

    assert [
        artifact.template
        for artifact in artifacts
    ] == [
        "documentation/communication_documentation.md.j2",
        "capabilities/communication_capabilities.md.j2",
    ]
