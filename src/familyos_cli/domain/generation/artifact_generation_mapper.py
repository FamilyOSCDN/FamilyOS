"""Artifact generation mapper."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_template_policy import (
    ArtifactTemplatePolicy,
    DefaultArtifactTemplatePolicy,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)


class ArtifactGenerationMapper:
    """Apply generation policies to domain artifacts."""

    def __init__(
        self,
        template_policy: ArtifactTemplatePolicy | None = None,
        profile: GenerationProfile = GenerationProfile.PYTHON_IMPLEMENTATION,
    ) -> None:
        """Initialize the mapper."""

        self._template_policy = (
            template_policy
            if template_policy is not None
            else DefaultArtifactTemplatePolicy()
        )

        self._profile = profile

    def map(
        self,
        artifact: ArtifactDefinition,
    ) -> ArtifactDefinition:
        """Apply template selection to an artifact."""

        return ArtifactDefinition(
            kind=artifact.kind,
            name=artifact.name,
            target_path=artifact.target_path,
            template=self._template_policy.template_for(
                kind=artifact.kind,
                current_template=artifact.template,
                profile=self._profile,
            ),
        )
