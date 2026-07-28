import pytest

from familyos_cli.domain.models.domain_specification import DomainSpecification
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)
from familyos_cli.shared.exceptions.specification_already_exists_error import (
    SpecificationAlreadyExistsError,
)


def create_spec(name: str) -> DomainSpecification:
    return DomainSpecification(
        name=name,
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )


def test_register_duplicate_specification() -> None:
    registry = DomainSpecificationRegistry()

    specification = create_spec("person")

    registry.register(specification)

    with pytest.raises(SpecificationAlreadyExistsError):
        registry.register(specification)


def test_get_all_specifications() -> None:
    registry = DomainSpecificationRegistry()

    registry.register(create_spec("person"))
    registry.register(create_spec("address"))

    specifications = registry.all()

    assert len(specifications) == 2
