from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.domain.models.domain_specification import DomainSpecification
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)


def test_register_and_get_specification() -> None:
    registry = DomainSpecificationRegistry()
    service = SpecificationService(registry)

    specification = DomainSpecification(
        name="person",
        entities=[],
        aggregates=[],
        repositories=[],
        services=[],
    )

    service.register(specification)

    assert service.contains("person")
    assert service.get("person") == specification