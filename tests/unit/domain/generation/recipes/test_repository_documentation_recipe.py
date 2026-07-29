from familyos_cli.domain.generation.recipes.repository_documentation_recipe import (
    RepositoryDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.models.repository_descriptor import (
    RepositoryDescriptor,
)


def test_repository_documentation_recipe_name() -> None:
    recipe = RepositoryDocumentationRecipe()

    assert recipe.name == "repository_documentation"


def test_repository_documentation_recipe_builds_artifacts() -> None:
    recipe = RepositoryDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                description="Person persistence repository",
                aggregate="Person",
                operations=[
                    "save",
                    "find",
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
        "repositories/personrepository/README.md"
        in paths
    )

    assert (
        "docs/30-domains/person/"
        "repositories/personrepository/"
        "Responsibilities.md"
        in paths
    )

    assert (
        "docs/30-domains/person/"
        "repositories/personrepository/"
        "Operations.md"
        in paths
    )

    assert (
        "docs/30-domains/person/"
        "repositories/personrepository/"
        "diagrams/"
        "persistence-flow.puml"
        in paths
    )
