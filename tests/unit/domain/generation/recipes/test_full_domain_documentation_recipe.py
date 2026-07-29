from familyos_cli.domain.generation.recipes.full_domain_documentation_recipe import (
    FullDomainDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_full_domain_documentation_recipe_name() -> None:
    recipe = FullDomainDocumentationRecipe()

    assert recipe.name == "full_domain_documentation"


def test_full_domain_documentation_recipe_combines_documentation_artifacts() -> None:
    recipe = FullDomainDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
        business_rules=[],
        entities=[],
        value_objects=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert len(artifacts) > 0

    templates = [
        artifact.template
        for artifact in artifacts
    ]

    assert "domain/README.md.j2" in templates
    assert "domain_context/Context.md.j2" in templates
