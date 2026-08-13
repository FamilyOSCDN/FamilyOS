from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.generation.recipes.aggregate_documentation_recipe import (
    AggregateDocumentationRecipe,
)
from familyos_cli.domain.models.aggregate_descriptor import (
    AggregateDescriptor,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


def test_aggregate_documentation_recipe_name() -> None:
    recipe = AggregateDocumentationRecipe()

    assert recipe.name == "aggregate_documentation"


def test_aggregate_documentation_recipe_builds_artifacts() -> None:
    recipe = AggregateDocumentationRecipe()

    specification = DomainSpecification(
        name="Person",
        aggregates=[
            AggregateDescriptor(
                name="PersonAggregate",
                description="Aggregate managing person lifecycle",
                root_entity="Person",
                entities=[
                    "Person",
                ],
                invariants=[
                    "Person must have a unique identity",
                ],
            )
        ],
    )

    artifacts = recipe.build_artifacts(
        specification,
    )

    assert recipe.profile == (
        GenerationProfile.DOMAIN_DOCUMENTATION
    )

    assert len(artifacts) == 4

    assert [
        artifact.kind
        for artifact in artifacts
    ] == [
        ArtifactKind.DOCUMENTATION,
    ] * 4

    assert [
        artifact.target_path
        for artifact in artifacts
    ] == [
        (
            "docs/30-domains/person/"
            "aggregates/personaggregate/README.md"
        ),
        (
            "docs/30-domains/person/"
            "aggregates/personaggregate/"
            "Responsibilities.md"
        ),
        (
            "docs/30-domains/person/"
            "aggregates/personaggregate/"
            "Invariants.md"
        ),
        (
            "docs/30-domains/person/"
            "aggregates/personaggregate/"
            "diagrams/lifecycle.puml"
        ),
    ]

    assert [
        artifact.template
        for artifact in artifacts
    ] == [
        "aggregate/README.md.j2",
        "aggregate/Responsibilities.md.j2",
        "aggregate/Invariants.md.j2",
        "aggregate/diagrams/lifecycle.puml.j2",
    ]

    aggregate = artifacts[0].context["aggregate"]

    assert isinstance(
        aggregate,
        AggregateDescriptor,
    )

    assert aggregate.name == "PersonAggregate"
