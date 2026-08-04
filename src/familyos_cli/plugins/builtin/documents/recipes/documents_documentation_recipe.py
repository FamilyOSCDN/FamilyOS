"""Documents documentation generation recipe."""

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


class DocumentsDocumentationRecipe:
    """Generate Documents documentation artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "documents-documentation"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build Documents documentation artifacts."""

        _ = specification

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name=(
                    "documents-domain-documentation"
                ),
                target_path=(
                    "docs/documents"
                ),
                template=(
                    "documents/documentation"
                ),
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name=(
                    "documents-capability-documentation"
                ),
                target_path=(
                    "docs/documents/capabilities"
                ),
                template=(
                    "documents/capabilities-documentation"
                ),
            ),
        ]
