"""Service documentation generation recipe."""

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


class ServiceDocumentationRecipe:
    """Build documentation artifacts for services."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "service_documentation"

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
        """Build service documentation artifacts."""

        slug = specification.name.strip().lower()

        artifacts: list[ArtifactDefinition] = []

        for service in specification.services:
            service_slug = (
                service.name.strip().lower()
            )

            base_path = (
                f"docs/30-domains/{slug}/"
                f"services/{service_slug}"
            )

            artifacts.extend(
                [
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{service.name} README"
                        ),
                        target_path=(
                            f"{base_path}/README.md"
                        ),
                        template=(
                            "service/README.md.j2"
                        ),
                        context={
                            "service": service,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{service.name} "
                            "Responsibilities"
                        ),
                        target_path=(
                            f"{base_path}/"
                            "Responsibilities.md"
                        ),
                        template=(
                            "service/"
                            "Responsibilities.md.j2"
                        ),
                        context={
                            "service": service,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{service.name} Operations"
                        ),
                        target_path=(
                            f"{base_path}/Operations.md"
                        ),
                        template=(
                            "service/"
                            "Operations.md.j2"
                        ),
                        context={
                            "service": service,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{service.name} "
                            "Interaction Flow"
                        ),
                        target_path=(
                            f"{base_path}/diagrams/"
                            "interaction-flow.puml"
                        ),
                        template=(
                            "service/"
                            "diagrams/"
                            "interaction-flow.puml.j2"
                        ),
                        context={
                            "service": service,
                        },
                    ),
                ],
            )

        return artifacts
