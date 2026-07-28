"""Artifact mapper contract."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)


class ArtifactMapper(Protocol):
    """Maps a domain artifact to an executable generation artifact."""

    def map(
        self,
        artifact: ArtifactDefinition,
    ) -> GenerationArtifact:
        """Create a generation artifact."""