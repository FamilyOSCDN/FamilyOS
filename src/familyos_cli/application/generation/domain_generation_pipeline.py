"""Domain generation pipeline."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.domain_generation_adapter import (
    DomainGenerationAdapter,
)
from familyos_cli.domain.generation.artifact_generation_mapper import (
    ArtifactGenerationMapper,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


class DomainGenerationPipeline:
    """Generate a domain from a specification."""

    def __init__(
        self,
        planner: DomainGenerationPlanner,
        mapper: ArtifactGenerationMapper,
        adapter: DomainGenerationAdapter,
        engine: GenerationEngine,
    ) -> None:
        self._planner = planner
        self._mapper = mapper
        self._adapter = adapter
        self._engine = engine

    def generate(
        self,
        specification: DomainSpecification,
        destination: Path,
    ) -> DomainGenerationPlan:
        """Generate domain artifacts."""

        plan = self._planner.create_plan(
            specification,
        )

        mapped_artifacts = [
            self._mapper.map(artifact)
            for artifact in plan.artifacts
        ]

        mapped_plan = DomainGenerationPlan(
            domain_name=plan.domain_name,
            artifacts=mapped_artifacts,
            metadata=plan.metadata,
        )

        project_specification = self._adapter.adapt(
            mapped_plan,
        )

        self._engine.generate(
            destination=destination,
            specification=project_specification,
            context={
                "domain_name": specification.name,
            },
        )

        return mapped_plan