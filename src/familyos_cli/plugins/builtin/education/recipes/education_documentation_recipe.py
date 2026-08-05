"""Education documentation generation recipe."""

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


class EducationDocumentationRecipe:
    """Generate education documentation artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "education-documentation"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build documentation artifacts."""

        _ = specification

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name=(
                    "education-domain-documentation"
                ),
                target_path=(
                    "docs/education"
                ),
                template=(
                    "education/documentation"
                ),
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name=(
                    "education-capability-documentation"
                ),
                target_path=(
                    "docs/education/capabilities"
                ),
                template=(
                    "education/capabilities-documentation"
                ),
            ),
        ]
