"""Specification registry."""

from pathlib import Path

from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)
from familyos_cli.infrastructure.specifications.specification_loader import (
    SpecificationLoader,
)
from familyos_cli.registry.artifact_registry import (
    ArtifactRegistry,
)


class SpecificationRegistry:
    """Provide specifications for registered artifacts."""

    def __init__(self) -> None:
        """Initialize the specification registry."""

        self._artifacts = ArtifactRegistry()
        self._loader = SpecificationLoader()

    def get(
        self,
        artifact_type: str,
    ) -> ProjectSpecification:
        """Return the specification for an artifact."""

        artifact = self._artifacts.get(
            artifact_type,
        )

        return self._loader.load(
            Path("specifications") / artifact.specification,
        )