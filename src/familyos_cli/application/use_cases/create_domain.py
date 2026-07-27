from __future__ import annotations

from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class CreateDomainUseCase:
    """Creates a domain generation plan."""

    def __init__(
        self,
        planner: DomainGenerationPlanner,
    ) -> None:
        self._planner = planner

    def execute(
        self,
        specification: DomainSpecification,
    ) -> DomainGenerationPlan:
        """Generate a domain plan from a specification."""

        return self._planner.create_plan(specification)