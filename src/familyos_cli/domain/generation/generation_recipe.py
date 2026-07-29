"""Generation recipe abstractions."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
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
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build artifacts produced by this recipe."""
