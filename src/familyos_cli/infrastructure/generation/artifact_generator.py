"""Artifact generator."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.infrastructure.specifications.specification_loader import (
    SpecificationLoader,
)
from familyos_cli.registry.artifact_registry import (
    ArtifactRegistry,
)


class ArtifactGenerator:
    """Generate artifacts from specifications."""

    def __init__(self) -> None:
        """Initialize the generator."""
        self._loader = SpecificationLoader()
        self._engine = GenerationEngine()
        self._registry = ArtifactRegistry()

    def generate(
        self,
        artifact_type: str,
        name: str,
    ) -> None:
        """Generate an artifact."""

        artifact = self._registry.get(
            artifact_type,
        )

        specification = self._loader.load(
            Path("specifications") / artifact.specification,
        )

        self._engine.generate(
            destination=Path(name),
            specification=specification,
            context={
                "name": name,
            },
        )
