"""Domain implementation generation strategy."""

from __future__ import annotations

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


class DomainImplementationStrategy:
    """Generate domain implementation artifacts."""

    def __init__(
        self,
        planner: DomainGenerationPlanner,
    ) -> None:
        """Initialize the strategy."""

        self._planner = planner

    @property
    def name(
        self,
    ) -> str:
        """Return strategy name."""

        return "domain_implementation"

    def supports(
        self,
        request: GenerationRequest,
    ) -> bool:
        """Check whether the strategy supports a request."""

        return request.recipe_name == self.name

    def execute(
        self,
        request: GenerationRequest,
        specification: DomainSpecification,
    ) -> DomainGenerationPlan:
        """Execute implementation generation."""

        return self._planner.create_plan(
            specification,
        )
