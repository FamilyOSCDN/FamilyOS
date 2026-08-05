"""Education domain generation recipe."""

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


class EducationDomainRecipe:
    """Generate education domain artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "education-domain"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build education artifacts."""

        _ = specification

        return [
            ArtifactDefinition(
                kind=ArtifactKind.ENTITY,
                name="education-domain-model",
                target_path=(
                    "education/models"
                ),
                template=(
                    "education/domain-model"
                ),
            ),
            ArtifactDefinition(
                kind=ArtifactKind.SERVICE,
                name="education-validation",
                target_path=(
                    "education/validation"
                ),
                template=(
                    "education/validation"
                ),
            ),
            ArtifactDefinition(
                kind=ArtifactKind.SERVICE,
                name="education-capabilities",
                target_path=(
                    "education/capabilities"
                ),
                template=(
                    "education/capabilities"
                ),
            ),
        ]
