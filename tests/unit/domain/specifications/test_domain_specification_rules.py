from __future__ import annotations

import pytest

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
from familyos_cli.domain.specifications.domain_specification_validator import (
    DomainSpecificationValidator,
)


def create_specification(
    *,
    name: str = "Person",
    entities: list[EntityDescriptor] | None = None,
) -> DomainSpecification:
    if entities is None:
        entities = [
            EntityDescriptor(
                name="Person",
            ),
        ]

    return DomainSpecification(
        name=name,
        entities=entities,
        aggregates=[
            AggregateDescriptor(
                name="PersonAggregate",
                description="",
                root_entity="Person",
            ),
        ],
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                description="",
                aggregate="PersonAggregate",
            ),
        ],
        services=[
            ServiceDescriptor(
                name="PersonService",
                description="",
            ),
        ],
        business_rules=[],
    )


def test_should_accept_valid_specification() -> None:
    validator = DomainSpecificationValidator()

    validator.validate(
        create_specification(),
    )


def test_should_reject_empty_name() -> None:
    validator = DomainSpecificationValidator()

    with pytest.raises(ValueError):
        validator.validate(
            create_specification(
                name="",
            ),
        )


def test_should_reject_without_entities() -> None:
    validator = DomainSpecificationValidator()

    with pytest.raises(ValueError):
        validator.validate(
            create_specification(
                entities=[],
            ),
        )


def test_should_reject_duplicate_entity_names() -> None:
    validator = DomainSpecificationValidator()

    entities = [
        EntityDescriptor(
            name="Person",
        ),
        EntityDescriptor(
            name="Person",
        ),
    ]

    with pytest.raises(ValueError):
        validator.validate(
            create_specification(
                entities=entities,
            ),
        )
