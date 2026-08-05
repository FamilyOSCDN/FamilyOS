from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.builtin.education.recipes import (
    EducationDocumentationRecipe,
)


def test_education_documentation_recipe_name() -> None:
    recipe = EducationDocumentationRecipe()

    assert recipe.name == (
        "education-documentation"
    )


def test_education_documentation_recipe_builds_artifacts() -> None:
    recipe = EducationDocumentationRecipe()

    artifacts = recipe.build_artifacts(
        DomainSpecification(
            name="Education",
        ),
    )

    names = {
        artifact.name
        for artifact in artifacts
    }

    assert (
        "education-domain-documentation"
        in names
    )

    assert (
        "education-capability-documentation"
        in names
    )
