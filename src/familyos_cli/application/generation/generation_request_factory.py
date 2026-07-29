"""Generation request factory."""

from __future__ import annotations

from familyos_cli.application.generation.preset_recipe_resolver import (
    PresetRecipeResolver,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


class GenerationRequestFactory:
    """Create generation requests."""

    def __init__(
        self,
        preset_recipe_resolver: PresetRecipeResolver | None = None,
    ) -> None:
        """Initialize the factory."""

        self._preset_recipe_resolver = (
            preset_recipe_resolver
        )

    def create(
        self,
        domain_name: str,
        recipe_name: str | None = None,
        preset: GenerationPreset | None = None,
    ) -> GenerationRequest:
        """Create a generation request."""

        resolved_recipe = recipe_name

        if (
            resolved_recipe is None
            and preset is not None
        ):
            if self._preset_recipe_resolver is None:
                raise ValueError(
                    "Preset resolver is required.",
                )

            resolved_recipe = (
                self._preset_recipe_resolver.resolve(
                    preset,
                )
            )

        if resolved_recipe is None:
            resolved_recipe = (
                "domain_documentation"
            )

        return GenerationRequest(
            domain_name=domain_name,
            recipe_name=resolved_recipe,
        )
