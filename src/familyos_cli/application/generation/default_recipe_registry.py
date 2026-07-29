"""Default generation recipe registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.recipes.aggregate_documentation_recipe import (
    AggregateDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.domain_context_documentation_recipe import (
    DomainContextDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.entity_documentation_recipe import (
    EntityDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.repository_documentation_recipe import (
    RepositoryDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.service_documentation_recipe import (
    ServiceDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.value_object_documentation_recipe import (
    ValueObjectDocumentationRecipe,
)


class DefaultRecipeRegistry:
    """Create the default generation recipe registry."""

    @staticmethod
    def create() -> GenerationRecipeRegistry:
        """Create a registry with built-in recipes."""

        registry = GenerationRecipeRegistry()

        registry.register(
            DomainDocumentationRecipe(),
        )

        registry.register(
            EntityDocumentationRecipe(),
        )

        registry.register(
            ValueObjectDocumentationRecipe(),
        )

        registry.register(
            AggregateDocumentationRecipe(),
        )

        registry.register(
            DomainContextDocumentationRecipe(),
        )

        registry.register(
            RepositoryDocumentationRecipe(),
        )

        registry.register(
            ServiceDocumentationRecipe(),
        )

        return registry
