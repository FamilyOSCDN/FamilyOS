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
from familyos_cli.application.generation.strategies.domain_context_documentation_strategy import (
    DomainContextDocumentationStrategy,
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
from familyos_cli.application.generation.strategies.full_domain_documentation_strategy import (
    FullDomainDocumentationStrategy,
)
from familyos_cli.application.generation.strategies.plugin_recipe_strategy import (
    PluginRecipeStrategy,
)
from familyos_cli.application.generation.strategies.repository_documentation_strategy import (
    RepositoryDocumentationStrategy,
)
from familyos_cli.application.generation.strategies.service_documentation_strategy import (
    ServiceDocumentationStrategy,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)


class DefaultGenerationStrategyRegistry:
    """Create the default generation strategy registry."""

    @staticmethod
    def create(
        recipe_registry: GenerationRecipeRegistry | None = None,
    ) -> GenerationStrategyRegistry:
        """Create registry with built-in strategies."""

        if recipe_registry is None:
            recipe_registry = DefaultRecipeRegistry.create()

        registry = GenerationStrategyRegistry()

        recipe_executor = RecipeExecutor(
            recipe_registry,
        )

        registry.register(
            DomainDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            EntityDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            AggregateDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            DomainContextDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            RepositoryDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            ServiceDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            FullDomainDocumentationStrategy(
                recipe_executor,
            ),
        )

        registry.register(
            DomainImplementationStrategy(
                DomainGenerationPlanner(),
            ),
        )

        registry.register(
            PluginRecipeStrategy(
                recipe_executor,
                recipe_registry,
            ),
        )

        return registry
