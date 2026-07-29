"""Generation preset definitions."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


@dataclass(frozen=True, slots=True)
class GenerationPresetDefinition:
    """Describe a generation preset."""

    preset: GenerationPreset

    recipes: tuple[str, ...]
