"""Factory for domain artifacts."""

from __future__ import annotations

from familyos_cli.domain.models.domain_artifact import DomainArtifact


class DomainArtifactFactory:
    """Create domain artifacts."""

    @staticmethod
    def create(
        name: str,
        description: str = "",
    ) -> DomainArtifact:
        """Create a domain artifact."""

        return DomainArtifact(
            name=name,
            description=description,
        )
