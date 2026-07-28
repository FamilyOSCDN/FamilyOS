"""Generation recipe abstractions."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)


class GenerationRecipe(Protocol):
    """Define a strategy for producing generation artifacts."""

    @property
    def name(
        self,
    ) -> str:
        """Return the recipe name."""

    def build_artifacts(
        self,
        domain_name: str,
    ) -> list[ArtifactDefinition]:
        """Build artifacts produced by this recipe."""
