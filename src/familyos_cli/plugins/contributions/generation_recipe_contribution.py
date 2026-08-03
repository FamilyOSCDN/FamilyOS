"""Generation recipe contribution contract."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_recipe import (
    GenerationRecipe,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)


@dataclass(
    frozen=True,
    slots=True,
)
class GenerationRecipeContribution(
    Contribution,
):
    """Contribution provided by a plugin for generation recipes."""

    recipe: GenerationRecipe
