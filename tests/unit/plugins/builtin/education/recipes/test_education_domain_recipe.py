from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.plugins.builtin.education.recipes import (
    EducationDomainRecipe,
)


def test_education_domain_recipe_name() -> None:
    recipe = EducationDomainRecipe()

    assert recipe.name == (
        "education-domain"
    )


def test_education_domain_recipe_builds_artifacts() -> None:
    recipe = EducationDomainRecipe()

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
        "education-domain-model"
        in names
    )

    assert (
        "education-validation"
        in names
    )

    assert (
        "education-capabilities"
        in names
    )
