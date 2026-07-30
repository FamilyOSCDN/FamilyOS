"""Generation contribution registry."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)


class GenerationContributionRegistry:
    """Registry of plugin generation contributions."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._contributions: dict[
            GenerationPresetId,
            GenerationContribution,
        ] = {}

    def register(
        self,
        contribution: GenerationContribution,
    ) -> None:
        """Register a generation contribution."""

        if contribution.preset in self._contributions:
            raise ValueError(
                (
                    "Generation contribution "
                    f"'{contribution.preset.value}' "
                    "already registered."
                ),
            )

        self._contributions[
            contribution.preset
        ] = contribution

    def get(
        self,
        preset: GenerationPresetId,
    ) -> GenerationContribution:
        """Return contribution for preset."""

        return self._contributions[preset]

    def list(
        self,
    ) -> tuple[GenerationContribution, ...]:
        """Return registered contributions."""

        return tuple(
            self._contributions.values(),
        )

    def all(
        self,
    ) -> tuple[GenerationContribution, ...]:
        """Return all registered contributions."""

        return tuple(
            self._contributions.values(),
        )
