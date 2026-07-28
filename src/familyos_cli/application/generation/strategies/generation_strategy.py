"""Generation strategy contract."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class GenerationStrategy(Protocol):
    """Contract for generation strategies."""

    @property
    def name(self) -> str:
        """Return strategy name."""

        ...

    def supports(
        self,
        request: GenerationRequest,
    ) -> bool:
        """Return whether the strategy supports a request."""

        ...

    def execute(
        self,
        request: GenerationRequest,
        specification: DomainSpecification,
    ) -> DomainGenerationPlan:
        """Execute generation strategy."""

        ...
