"""Domain generation pipeline."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.application.ports.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainGenerationPipeline:
    """Generate a domain from a specification."""

    def __init__(
        self,
        planner: DomainGenerationPlanner,
        specification_mapper: GenerationSpecificationMapper,
        engine: GenerationEngine,
    ) -> None:
        """Initialize the pipeline."""

        self._planner = planner
        self._specification_mapper = specification_mapper
        self._engine = engine

    def generate(
        self,
        specification: DomainSpecification,
        destination: Path,
    ) -> GenerationSpecification:
        """Generate domain artifacts."""

        plan = self._planner.create_plan(
            specification,
        )

        generation_specification = self._specification_mapper.map(
            plan,
        )

        self._engine.generate(
            destination=destination,
            specification=generation_specification,
            context={
                "domain_name": specification.name,
            },
        )

        return generation_specification
