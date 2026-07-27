from unittest.mock import Mock

from familyos_cli.application.specifications import (
    DomainSpecificationLoaderService,
    SpecificationService,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)


def test_load_and_register_specification() -> None:
    specification = DomainSpecification(
        name="Person",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    loader = Mock()
    loader.load.return_value = specification

    registry = DomainSpecificationRegistry()

    service = SpecificationService(
        registry,
    )

    loader_service = DomainSpecificationLoaderService(
        loader,
        service,
    )

    result = loader_service.load(
        "person.yaml",
    )

    assert result == specification
    assert service.contains("Person")