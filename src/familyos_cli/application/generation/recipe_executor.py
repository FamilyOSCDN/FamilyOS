"""Generation recipe executor."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.generation_recipe_registry import (
    GenerationRecipeRegistry,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


class RecipeExecutor:
    """Execute generation recipes."""

    def __init__(
        self,
        registry: GenerationRecipeRegistry,
    ) -> None:
        """Initialize the executor."""

        self._registry = registry

    def execute(
        self,
        request: GenerationRequest,
    ) -> list[ArtifactDefinition]:
        """Execute the recipe associated with a request."""

        recipe = self._registry.get(
            request.recipe_name,
        )

        return recipe.build_artifacts(
            request.domain_name,
        )
