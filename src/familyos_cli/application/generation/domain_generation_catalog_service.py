"""Domain generation catalog service."""

from __future__ import annotations

from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)


class DomainGenerationCatalogService:
    """Provide access to domain generation contributions."""

    def __init__(
        self,
        domain_contributions: tuple[
            DomainGenerationContribution,
            ...,
        ] = (),
    ) -> None:
        """Initialize service."""

        self._contributions = domain_contributions

    def list_domains(
        self,
    ) -> tuple[DomainGenerationContribution, ...]:
        """Return available generation domains."""

        return self._contributions
