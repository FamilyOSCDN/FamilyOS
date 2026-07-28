"""Domain generation pipeline."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.application.ports.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainGenerationPipeline:
    """Generate a domain from a generation request."""

    def __init__(
        self,
        planner: DomainGenerationPlanner,
        specification_mapper: GenerationSpecificationMapper,
        engine: GenerationEngine,
        recipe_executor: RecipeExecutor,
    ) -> None:
        """Initialize the pipeline."""

        self._planner = planner

        self._specification_mapper = specification_mapper

        self._engine = engine

        self._recipe_executor = recipe_executor

    def generate(
        self,
        request: GenerationRequest,
        specification: DomainSpecification,
        destination: Path,
    ) -> GenerationSpecification:
        """Generate domain artifacts."""

        artifacts = self._recipe_executor.execute(
            request,
        )

        plan = DomainGenerationPlan(
            domain_name=request.domain_name,
            artifacts=artifacts,
        )

        generation_specification = self._specification_mapper.map(
            plan,
        )

        self._engine.generate(
            destination=destination,
            specification=generation_specification,
            context={
                "domain_name": request.domain_name,
                "name": request.domain_name,
                "recipe_name": request.recipe_name,
            },
        )

        return generation_specification
