from __future__ import annotations

from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)


class CreateDomainUseCase:
    """Creates a domain generation plan."""

    def __init__(
        self,
        planner: DomainGenerationPlanner,
        get_specification: GetDomainSpecificationUseCase,
    ) -> None:
        self._planner = planner
        self._get_specification = get_specification

    def execute(
        self,
        domain_name: str,
    ) -> DomainGenerationPlan | None:
        """Generate a domain plan from a domain name."""

        specification = self._get_specification.execute(domain_name)

        if specification is None:
            return None

        return self._planner.create_plan(specification)