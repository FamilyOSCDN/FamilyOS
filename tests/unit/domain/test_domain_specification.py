from familyos_cli.domain.models.aggregate_descriptor import (
    AggregateDescriptor,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.models.entity_descriptor import (
    EntityDescriptor,
)
from familyos_cli.domain.models.repository_descriptor import (
    RepositoryDescriptor,
)
from familyos_cli.domain.models.service_descriptor import (
    ServiceDescriptor,
)


def test_domain_specification_creation() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(
                name="Person",
                description="Represents a person in the family domain.",
            )
        ],
        aggregates=[
            AggregateDescriptor(
                name="Person",
                root_entity="Person",
                description="Person aggregate root.",
            )
        ],
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                aggregate="Person",
                description="Repository for person persistence.",
            )
        ],
        services=[
            ServiceDescriptor(
                name="PersonService",
                description="Application service for person operations.",
            )
        ],
    )

    assert specification.name == "Person"
    assert len(specification.entities) == 1
    assert specification.entities[0].name == "Person"

    assert len(specification.aggregates) == 1
    assert specification.aggregates[0].root_entity == "Person"

    assert len(specification.repositories) == 1
    assert specification.repositories[0].name == "PersonRepository"

    assert len(specification.services) == 1
    assert specification.services[0].name == "PersonService"


def test_domain_specification_is_immutable() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    try:
        specification.name = "Family"
    except AttributeError:
        assert True
    else:
        raise AssertionError("Expected code path was not reached.")
