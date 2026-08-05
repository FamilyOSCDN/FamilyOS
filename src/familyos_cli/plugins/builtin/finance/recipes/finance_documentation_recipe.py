"""Finance documentation generation recipe."""

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


class FinanceDocumentationRecipe:
    """Build finance documentation artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "finance_documentation"

    @property
    def profile(
        self,
    ) -> GenerationProfile:
        """Return generation profile."""

        return GenerationProfile.DOMAIN_DOCUMENTATION

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build finance documentation artifacts."""

        slug = specification.name.strip().lower()

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Finance",
                target_path=(
                    f"docs/30-domains/{slug}/Finance.md"
                ),
                template="Finance.md.j2",
            ),
        ]
