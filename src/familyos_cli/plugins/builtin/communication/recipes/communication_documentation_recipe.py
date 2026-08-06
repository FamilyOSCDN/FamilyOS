"""Communication documentation generation recipe."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class CommunicationDocumentationRecipe:
    """Generate Communication documentation artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "communication-documentation"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build Communication documentation artifacts."""

        _ = specification

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name=(
                    "communication-domain-documentation"
                ),
                target_path=(
                    "docs/communication"
                ),
                template=(
                    "documentation/"
                    "communication_documentation.md.j2"
                ),
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name=(
                    "communication-capability-documentation"
                ),
                target_path=(
                    "docs/communication/capabilities"
                ),
                template=(
                    "capabilities/"
                    "communication_capabilities.md.j2"
                ),
            ),
        ]
