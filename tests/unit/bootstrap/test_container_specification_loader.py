from familyos_cli.application.specifications.domain_specification_loader_service import (
    DomainSpecificationLoaderService,
)
from familyos_cli.bootstrap.container import ApplicationContainer


def test_should_create_domain_specification_loader_service() -> None:
    container = ApplicationContainer()

    service = container.domain_specification_loader_service()

    assert isinstance(
        service,
        DomainSpecificationLoaderService,
    )
