"""Artifact generation mapper."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)


class ArtifactGenerationMapper:
    """Resolve templates for domain artifacts."""

    TEMPLATE_MAPPING = {
        "entity": "entity.py.jinja",
        "aggregate": "aggregate.py.jinja",
        "repository": "repository.py.jinja",
        "service": "service.py.jinja",
    }

    def map(
        self,
        artifact: ArtifactDefinition,
    ) -> ArtifactDefinition:
        """Apply template mapping to an artifact."""

        return ArtifactDefinition(
            artifact_type=artifact.artifact_type,
            name=artifact.name,
            target_path=artifact.target_path,
            template=self.TEMPLATE_MAPPING.get(
                artifact.artifact_type,
                artifact.template,
            ),
        )