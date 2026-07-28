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
from familyos_cli.domain.validation.domain_specification_validator import (
    DomainSpecificationValidator,
)


def test_valid_domain_specification() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(
                name="Person",
                description="Person entity.",
            )
        ],
        aggregates=[
            AggregateDescriptor(
                name="Person",
                root_entity="Person",
                description="Person aggregate.",
            )
        ],
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                aggregate="Person",
                description="Person repository.",
            )
        ],
        services=[
            ServiceDescriptor(
                name="PersonService",
                description="Person service.",
            )
        ],
    )

    validator = DomainSpecificationValidator()

    validator.validate(specification)


def test_empty_domain_name_is_rejected() -> None:
    specification = DomainSpecification(
        name="",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    validator = DomainSpecificationValidator()

    with pytest.raises(ValueError):
        validator.validate(specification)


def test_duplicate_entities_are_rejected() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(name="Person"),
            EntityDescriptor(name="Person"),
        ],
        aggregates=[],
        repositories=[],
        services=[],
    )

    validator = DomainSpecificationValidator()

    with pytest.raises(ValueError):
        validator.validate(specification)


def test_unknown_aggregate_root_is_rejected() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(name="Person"),
        ],
        aggregates=[
            AggregateDescriptor(
                name="Person",
                root_entity="Unknown",
                description="Invalid aggregate.",
            )
        ],
        repositories=[],
        services=[],
    )

    validator = DomainSpecificationValidator()

    with pytest.raises(ValueError):
        validator.validate(specification)


def test_unknown_repository_aggregate_is_rejected() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[
            EntityDescriptor(name="Person"),
        ],
        aggregates=[
            AggregateDescriptor(
                name="Person",
                root_entity="Person",
                description="Person aggregate.",
            )
        ],
        repositories=[
            RepositoryDescriptor(
                name="PersonRepository",
                aggregate="Unknown",
                description="Invalid repository.",
            )
        ],
        services=[],
    )

    validator = DomainSpecificationValidator()

    with pytest.raises(ValueError):
        validator.validate(specification)
