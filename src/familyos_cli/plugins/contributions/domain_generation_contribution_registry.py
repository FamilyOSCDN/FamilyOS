"""Domain generation contribution registry."""

from __future__ import annotations

from familyos_cli.plugins.contributions.domain_generation_contribution import (
    DomainGenerationContribution,
)


class DomainGenerationContributionRegistry:
    """Registry of plugin domain generation contributions."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._contributions: dict[
            str,
            DomainGenerationContribution,
        ] = {}

    def register(
        self,
        contribution: DomainGenerationContribution,
    ) -> None:
        """Register a domain generation contribution."""

        if contribution.domain in self._contributions:
            raise ValueError(
                (
                    f"Domain generation contribution "
                    f"'{contribution.domain}' "
                    "already registered."
                ),
            )

        self._contributions[
            contribution.domain
        ] = contribution

    def get(
        self,
        domain: str,
    ) -> DomainGenerationContribution:
        """Return contribution for a domain."""

        return self._contributions[domain]

    def list(
        self,
    ) -> tuple[DomainGenerationContribution, ...]:
        """Return registered contributions."""

        return tuple(
            self._contributions.values(),
        )

    def all(
        self,
    ) -> tuple[DomainGenerationContribution, ...]:
        """Return all registered contributions."""

        return tuple(
            self._contributions.values(),
        )
