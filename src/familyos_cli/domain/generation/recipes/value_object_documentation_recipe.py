"""Value object documentation generation recipe."""

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


class ValueObjectDocumentationRecipe:
    """Build documentation artifacts for value objects."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "value_object_documentation"

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
        """Build value object documentation artifacts."""

        slug = specification.name.strip().lower()

        return [
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Value Objects README",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "value_objects/README.md"
                ),
                template="value_object/README.md.j2",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Value Object Attributes",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "value_objects/Attributes.md"
                ),
                template="value_object/Attributes.md.j2",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Value Object Responsibilities",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "value_objects/Responsibilities.md"
                ),
                template="value_object/Responsibilities.md.j2",
            ),
            ArtifactDefinition(
                kind=ArtifactKind.DOCUMENTATION,
                name="Value Object Business Rules",
                target_path=(
                    f"docs/30-domains/{slug}/"
                    "value_objects/Business-Rules.md"
                ),
                template="value_object/Business-Rules.md.j2"
            ),
        ]
