"""Generation contribution contract."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)


@dataclass(
    frozen=True,
    slots=True,
)
class GenerationContribution(
    Contribution,
):
    """Contribution provided by a plugin."""

    preset: GenerationPresetId

    description: str

    recipes: tuple[str, ...]
