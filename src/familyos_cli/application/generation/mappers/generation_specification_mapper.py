"""Generation specification mapper."""

from __future__ import annotations

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.mappers.default_artifact_mapper import (
    DefaultArtifactMapper,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)


class GenerationSpecificationMapper:
    """Maps generation plans into execution specifications."""

    def __init__(
        self,
    ) -> None:
        """Initialize mapper."""

        self._artifact_mapper = DefaultArtifactMapper()

    def map(
        self,
        plan: DomainGenerationPlan,
    ) -> GenerationSpecification:
        """Transform a generation plan into a specification."""

        artifacts = [
            self._artifact_mapper.map(
                artifact,
            )
            for artifact in plan.artifacts
        ]

        return GenerationSpecification(
            artifacts=artifacts,
        )
