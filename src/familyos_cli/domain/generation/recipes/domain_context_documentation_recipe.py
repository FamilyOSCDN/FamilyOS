"""Domain context documentation generation recipe."""

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


class DomainContextDocumentationRecipe:
    """Build context documentation artifacts for a domain."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "domain_context_documentation"

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
        """Build domain context documentation artifacts."""

        slug = specification.name.strip().lower()

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Domain Context",
                target_path=(
                    f"docs/30-domains/{slug}/Context.md"
                ),
                template="domain_context/Context.md.j2",
                context={
                    "domain": specification,
                },
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Domain Responsibilities",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "Responsibilities.md"
                ),
                template=(
                    "domain_context/"
                    "Responsibilities.md.j2"
                ),
                context={
                    "domain": specification,
                },
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Domain Integrations",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "Integrations.md"
                ),
                template=(
                    "domain_context/"
                    "Integrations.md.j2"
                ),
                context={
                    "domain": specification,
                },
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Domain Business Rules",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "Business-Rules.md"
                ),
                template=(
                    "domain_context/"
                    "Business-Rules.md.j2"
                ),
                context={
                    "domain": specification,
                },
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Domain Context Map",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "diagrams/context-map.puml"
                ),
                template=(
                    "domain_context/"
                    "diagrams/context-map.puml.j2"
                ),
                context={
                    "domain": specification,
                },
            ),
        ]
