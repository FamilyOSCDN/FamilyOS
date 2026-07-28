from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)


def test_get_domain_specification() -> None:
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

    use_case = GetDomainSpecificationUseCase(service)

    result = use_case.execute("person")

    assert result == specification
