"""Artifact template selection policies."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)


class ArtifactTemplatePolicy(Protocol):
    """Define how templates are selected for artifacts."""

    def template_for(
        self,
        kind: ArtifactKind,
        current_template: str = "",
    ) -> str:
        """Return the template assigned to an artifact."""


class DefaultArtifactTemplatePolicy:
    """Select conventional templates for generated artifacts."""

    _TEMPLATES: dict[ArtifactKind, str] = {
        ArtifactKind.ENTITY: "entity.py.jinja",
        ArtifactKind.VALUE_OBJECT: "value_object.py.jinja",
        ArtifactKind.AGGREGATE: "aggregate.py.jinja",
        ArtifactKind.REPOSITORY: "repository.py.jinja",
        ArtifactKind.SERVICE: "service.py.jinja",
    }

    def template_for(
        self,
        kind: ArtifactKind,
        current_template: str = "",
    ) -> str:
        """Return the configured template for an artifact."""

        return self._TEMPLATES.get(
            kind,
            current_template,
        )
