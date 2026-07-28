"""Artifact template selection policies."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)


class ArtifactTemplatePolicy(Protocol):
    """Define how templates are selected for artifacts."""

    def template_for(
        self,
        kind: ArtifactKind,
        current_template: str = "",
        profile: GenerationProfile = GenerationProfile.PYTHON_IMPLEMENTATION,
    ) -> str:
        """Return the template assigned to an artifact."""


class DefaultArtifactTemplatePolicy:
    """Select conventional templates for generated artifacts."""

    _PYTHON_TEMPLATES: dict[ArtifactKind, str] = {
        ArtifactKind.ENTITY: "entity.py.jinja",
        ArtifactKind.VALUE_OBJECT: "value_object.py.jinja",
        ArtifactKind.AGGREGATE: "aggregate.py.jinja",
        ArtifactKind.REPOSITORY: "repository.py.jinja",
        ArtifactKind.SERVICE: "service.py.jinja",
    }

    _DOCUMENTATION_TEMPLATES: dict[ArtifactKind, str] = {
        ArtifactKind.ENTITY: "entity/README.md.j2",
        ArtifactKind.AGGREGATE: "aggregate/README.md.j2",
    }

    def template_for(
        self,
        kind: ArtifactKind,
        current_template: str = "",
        profile: GenerationProfile = GenerationProfile.PYTHON_IMPLEMENTATION,
    ) -> str:
        """Return the configured template for an artifact."""

        if profile is GenerationProfile.DOMAIN_DOCUMENTATION:
            return self._DOCUMENTATION_TEMPLATES.get(
                kind,
                current_template,
            )

        return self._PYTHON_TEMPLATES.get(
            kind,
            current_template,
        )
