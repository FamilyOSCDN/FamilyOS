"""Domain generation service."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.generation.directory_layout import (
    DirectoryLayout,
)
from familyos_cli.domain.generation.domain_context import (
    DomainContext,
)
from familyos_cli.domain.generation.template_provider import (
    TemplateProvider,
)
from familyos_cli.domain.models.domain_artifact import (
    DomainArtifact,
)


class DomainGenerator:
    """Generate domain generation instructions."""

    def __init__(
        self,
        layout: DirectoryLayout | None = None,
        template_provider: TemplateProvider | None = None,
    ) -> None:
        """Initialize domain generator."""

        self._layout = layout or DirectoryLayout()
        self._template_provider = (
            template_provider
            or TemplateProvider()
        )

    def generate(
        self,
        artifact: DomainArtifact,
    ) -> DomainContext:
        """Create a generation context for a domain."""

        return DomainContext(
            name=artifact.name,
            slug=artifact.normalized_name,
            namespace=artifact.normalized_name,
            title=artifact.display_name,
            description=artifact.description,
        )

    def directories(
        self,
        artifact: DomainArtifact,
    ) -> tuple[Path, ...]:
        """Return directories required by the domain."""

        return self._layout.directories(
            artifact.normalized_name,
        )

    def templates(
        self,
    ) -> tuple[str, ...]:
        """Return templates used for generation."""

        return self._template_provider.templates()