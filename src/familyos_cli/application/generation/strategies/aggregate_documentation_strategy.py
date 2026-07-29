"""Aggregate documentation generation strategy."""

from __future__ import annotations

from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class AggregateDocumentationStrategy:
    """Generate aggregate documentation artifacts."""

    def __init__(
        self,
        recipe_executor: RecipeExecutor,
    ) -> None:
        """Initialize the strategy."""

        self._recipe_executor = recipe_executor

    @property
    def name(
        self,
    ) -> str:
        """Return strategy name."""

        return "aggregate_documentation"

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
        """Execute aggregate documentation generation."""

        return DomainGenerationPlan(
            domain_name=specification.name,
            artifacts=self._recipe_executor.execute(
                request,
                specification,
            ),
            metadata={
                "strategy": self.name,
            },
        )
