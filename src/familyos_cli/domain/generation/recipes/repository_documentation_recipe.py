"""Repository documentation generation recipe."""

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


class RepositoryDocumentationRecipe:
    """Build documentation artifacts for repositories."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "repository_documentation"

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
        """Build repository documentation artifacts."""

        slug = specification.name.strip().lower()

        artifacts: list[ArtifactDefinition] = []

        for repository in specification.repositories:
            repository_slug = (
                repository.name.strip().lower()
            )

            base_path = (
                f"docs/30-domains/{slug}/"
                f"repositories/{repository_slug}"
            )

            artifacts.extend(
                [
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{repository.name} README"
                        ),
                        target_path=(
                            f"{base_path}/README.md"
                        ),
                        template=(
                            "repository/README.md.j2"
                        ),
                        context={
                            "repository": repository,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{repository.name} "
                            "Responsibilities"
                        ),
                        target_path=(
                            f"{base_path}/Responsibilities.md"
                        ),
                        template=(
                            "repository/"
                            "Responsibilities.md.j2"
                        ),
                        context={
                            "repository": repository,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{repository.name} Operations"
                        ),
                        target_path=(
                            f"{base_path}/Operations.md"
                        ),
                        template=(
                            "repository/"
                            "Operations.md.j2"
                        ),
                        context={
                            "repository": repository,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{repository.name} "
                            "Persistence Flow"
                        ),
                        target_path=(
                            f"{base_path}/diagrams/"
                            "persistence-flow.puml"
                        ),
                        template=(
                            "repository/"
                            "diagrams/"
                            "persistence-flow.puml.j2"
                        ),
                        context={
                            "repository": repository,
                        },
                    ),
                ],
            )

        return artifacts
