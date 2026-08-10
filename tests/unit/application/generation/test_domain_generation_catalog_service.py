from familyos_cli.application.generation.domain_generation_catalog_service import (
    DomainGenerationCatalogService,
)
from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


def test_service_returns_domain_generation_contributions() -> None:
    contribution = DomainGenerationContribution(
        id=PluginContributionId(
            "familyos.test.domain.health",
        ),
        domain="Health",
        description="Health domain generation.",
        artifacts=(
            "health_documentation",
            "health_domain_model",
        ),
    )

    service = DomainGenerationCatalogService(
        domain_contributions=(
            contribution,
        ),
    )

    domains = service.list_domains()

    assert domains == (
        contribution,
    )


def test_service_returns_empty_domains_by_default() -> None:
    service = DomainGenerationCatalogService()

    domains = service.list_domains()

    assert domains == ()
