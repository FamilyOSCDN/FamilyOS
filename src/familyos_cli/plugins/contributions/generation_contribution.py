"""Generation contribution contract."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


@dataclass(frozen=True, slots=True)
class GenerationContribution:
    """Contribution provided by a plugin."""

    preset: GenerationPreset

    description: str

    recipes: tuple[str, ...]
