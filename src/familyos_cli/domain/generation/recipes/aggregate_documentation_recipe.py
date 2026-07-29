"""Aggregate documentation generation recipe."""

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


class AggregateDocumentationRecipe:
    """Build documentation artifacts for aggregates."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

        return "aggregate_documentation"

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
        """Build aggregate documentation artifacts."""

        slug = specification.name.strip().lower()

        artifacts: list[ArtifactDefinition] = []

        for aggregate in specification.aggregates:
            aggregate_slug = (
                aggregate.name.strip().lower()
            )

            base_path = (
                f"docs/30-domains/{slug}/"
                f"aggregates/{aggregate_slug}"
            )

            artifacts.extend(
                [
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{aggregate.name} README"
                        ),
                        target_path=(
                            f"{base_path}/README.md"
                        ),
                        template=(
                            "aggregate/README.md.j2"
                        ),
                        context={
                            "aggregate": aggregate,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{aggregate.name} "
                            "Responsibilities"
                        ),
                        target_path=(
                            f"{base_path}/Responsibilities.md"
                        ),
                        template=(
                            "aggregate/"
                            "Responsibilities.md.j2"
                        ),
                        context={
                            "aggregate": aggregate,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{aggregate.name} Invariants"
                        ),
                        target_path=(
                            f"{base_path}/Invariants.md"
                        ),
                        template=(
                            "aggregate/"
                            "Invariants.md.j2"
                        ),
                        context={
                            "aggregate": aggregate,
                        },
                    ),
                    ArtifactDefinition(
                        kind=ArtifactKind.DOCUMENTATION,
                        name=(
                            f"{aggregate.name} Lifecycle"
                        ),
                        target_path=(
                            f"{base_path}/diagrams/"
                            "lifecycle.puml"
                        ),
                        template=(
                            "aggregate/"
                            "diagrams/lifecycle.puml.j2"
                        ),
                        context={
                            "aggregate": aggregate,
                        },
                    ),
                ],
            )

        return artifacts
