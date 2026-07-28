"""Default artifact mapper."""

from __future__ import annotations

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)


class DefaultArtifactMapper:
    """Default implementation of artifact mapping."""

    def map(
        self,
        artifact: ArtifactDefinition,
    ) -> GenerationArtifact:
        """Transform an artifact definition into a generation artifact."""

        return GenerationArtifact(
            template=artifact.template,
            destination=artifact.target_path,
            context=GenerationContext(
                variables=artifact.context,
            ),
        )
