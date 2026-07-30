from familyos_cli.application.generation.domain_generation_catalog_service import (
    DomainGenerationCatalogService,
)
from familyos_cli.bootstrap.container import (
    ApplicationContainer,
)


def test_container_provides_domain_generation_catalog_service() -> None:
    container = ApplicationContainer()

    service = (
        container.domain_generation_catalog_service()
    )

    assert isinstance(
        service,
        DomainGenerationCatalogService,
    )


def test_container_domain_generation_catalog_is_empty_without_plugins() -> None:
    container = ApplicationContainer()

    service = (
        container.domain_generation_catalog_service()
    )

    assert service.list_domains() == ()
