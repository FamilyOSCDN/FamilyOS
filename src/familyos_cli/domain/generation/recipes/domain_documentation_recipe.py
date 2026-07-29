"""Domain documentation generation recipe."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainDocumentationRecipe:
    """Build documentation artifacts for a domain."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "domain_documentation"

    @property
    def profile(
        self,
    ) -> GenerationProfile:
        """Return the generation profile."""

        return GenerationProfile.DOMAIN_DOCUMENTATION

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build domain documentation artifacts."""

        slug = specification.name.strip().lower()

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="README",
                target_path=f"docs/30-domains/{slug}/README.md",
                template="domain/README.md.j2",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Vision",
                target_path=f"docs/30-domains/{slug}/Vision.md",
                template="domain/Vision.md.j2",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Capabilities",
                target_path=f"docs/30-domains/{slug}/Capabilities.md",
                template="domain/Capabilities.md.j2",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Domain Model",
                target_path=f"docs/30-domains/{slug}/Domain-Model.md",
                template="domain/Domain-Model.md.j2",
            ),
        ]
