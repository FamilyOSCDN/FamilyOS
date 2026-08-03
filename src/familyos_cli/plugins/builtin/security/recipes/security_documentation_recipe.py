"""Security documentation generation recipe."""

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


class SecurityDocumentationRecipe:
    """Build security documentation artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "security_documentation"

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
        """Build security documentation artifacts."""

        slug = specification.name.strip().lower()

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Security",
                target_path=(
                    f"docs/30-domains/{slug}/Security.md"
                ),
                template="Security.md.j2",
            ),
        ]
