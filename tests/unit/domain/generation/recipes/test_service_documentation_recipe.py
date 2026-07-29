from familyos_cli.domain.generation.recipes.service_documentation_recipe import (
    ServiceDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.models.service_descriptor import (
    ServiceDescriptor,
)


def test_service_documentation_recipe_name() -> None:
    recipe = ServiceDocumentationRecipe()

    assert recipe.name == "service_documentation"


def test_service_documentation_recipe_builds_artifacts() -> None:
    recipe = ServiceDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
        services=[
            ServiceDescriptor(
                name="PersonService",
                description="Person domain service",
                responsibilities=[
                    "Manage person operations",
                    "Coordinate domain workflows",
                ],
            ),
        ],
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert len(artifacts) == 4

    paths = {
        artifact.target_path
        for artifact in artifacts
    }

    assert (
        "docs/30-domains/person/"
        "services/personservice/README.md"
        in paths
    )

    assert (
        "docs/30-domains/person/"
        "services/personservice/"
        "Responsibilities.md"
        in paths
    )

    assert (
        "docs/30-domains/person/"
        "services/personservice/"
        "Operations.md"
        in paths
    )

    assert (
        "docs/30-domains/person/"
        "services/personservice/"
        "diagrams/"
        "interaction-flow.puml"
        in paths
    )
