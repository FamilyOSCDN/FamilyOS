"""Entity documentation generation recipe."""

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


class EntityDocumentationRecipe:
    """Build documentation artifacts for entities."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "entity_documentation"

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
        """Build entity documentation artifacts."""

        slug = specification.name.strip().lower()

        artifacts: list[ArtifactDefinition] = []

        for entity in specification.entities:
            entity_slug = entity.name.strip().lower()

            base_path = (
                f"docs/30-domains/{slug}/"
                f"entities/{entity_slug}"
            )

            context = {
                "entity": entity,
            }

            artifacts.extend(
                [
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=f"{entity.name} README",
                        target_path=(
                            f"{base_path}/README.md"
                        ),
                        template="entity/README.md.j2",
                        context=context,
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=f"{entity.name} Attributes",
                        target_path=(
                            f"{base_path}/Attributes.md"
                        ),
                        template="entity/Attributes.md.j2",
                        context=context,
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{entity.name} Responsibilities"
                        ),
                        target_path=(
                            f"{base_path}/Responsibilities.md"
                        ),
                        template=(
                            "entity/Responsibilities.md.j2"
                        ),
                        context=context,
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{entity.name} Business Rules"
                        ),
                        target_path=(
                            f"{base_path}/Business-Rules.md"
                        ),
                        template=(
                            "entity/Business-Rules.md.j2"
                        ),
                        context=context,
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{entity.name} Relationships"
                        ),
                        target_path=(
                            f"{base_path}/Relationships.md"
                        ),
                        template=(
                            "entity/Relationships.md.j2"
                        ),
                        context=context,
                    ),
                ],
            )

        return artifacts
