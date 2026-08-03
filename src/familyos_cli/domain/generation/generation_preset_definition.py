"""Generation preset definitions."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


@dataclass(frozen=True, slots=True)
class GenerationPresetDefinition:
    """Describe a generation preset."""

    preset: GenerationPresetId | GenerationPreset

    recipes: tuple[str, ...]

    def preset_id(
        self,
    ) -> GenerationPresetId:
        """Return the normalized preset identifier."""

        if isinstance(
            self.preset,
            GenerationPresetId,
        ):
            return self.preset

        return GenerationPresetId(
            self.preset.value,
        )
