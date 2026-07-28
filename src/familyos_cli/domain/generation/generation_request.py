"""Generation request model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """Describe a generation request."""

    domain_name: str

    recipe_name: str

    profile: GenerationProfile = (
        GenerationProfile.PYTHON_IMPLEMENTATION
    )
