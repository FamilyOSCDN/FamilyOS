"""Default generation strategy registry."""

from __future__ import annotations

from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)
from familyos_cli.application.generation.generation_strategy_registry import (
    GenerationStrategyRegistry,
)
from familyos_cli.application.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.application.generation.strategies.aggregate_documentation_strategy import (
    AggregateDocumentationStrategy,
)
from familyos_cli.application.generation.strategies.domain_documentation_strategy import (
    DomainDocumentationStrategy,
)
from familyos_cli.application.generation.strategies.domain_implementation_strategy import (
    DomainImplementationStrategy,
)
from familyos_cli.application.generation.strategies.entity_documentation_strategy import (
    EntityDocumentationStrategy,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)


class DefaultGenerationStrategyRegistry:
    """Create the default generation strategy registry."""

    @staticmethod
    def create() -> GenerationStrategyRegistry:
        """Create registry with built-in strategies."""

        registry = GenerationStrategyRegistry()

        registry.register(
            DomainDocumentationStrategy(
                RecipeExecutor(
                    DefaultRecipeRegistry.create(),
                ),
            ),
        )

        registry.register(
            EntityDocumentationStrategy(
                RecipeExecutor(
                    DefaultRecipeRegistry.create(),
                ),
            ),
        )

        registry.register(
            AggregateDocumentationStrategy(
                RecipeExecutor(
                    DefaultRecipeRegistry.create(),
                ),
            ),
        )

        registry.register(
            DomainImplementationStrategy(
                DomainGenerationPlanner(),
            ),
        )

        return registry
