"""Plugin recipe generation strategy."""

from __future__ import annotations

from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class PluginRecipeStrategy:
    """Execute plugin provided generation recipes."""

    def __init__(
        self,
        recipe_executor: RecipeExecutor,
        recipe_registry: GenerationRecipeRegistry,
    ) -> None:
        """Initialize the strategy."""

        self._recipe_executor = recipe_executor
        self._recipe_registry = recipe_registry

    @property
    def name(
        self,
    ) -> str:
        """Return strategy name."""

        return "plugin_recipe"

    def supports(
        self,
        request: GenerationRequest,
    ) -> bool:
        """Check whether a recipe is available."""

        try:
            self._recipe_registry.get(
                request.recipe_name,
            )

        except ValueError:
            return False

        return True

    def execute(
        self,
        request: GenerationRequest,
        specification: DomainSpecification,
    ) -> DomainGenerationPlan:
        """Execute plugin recipe."""

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
