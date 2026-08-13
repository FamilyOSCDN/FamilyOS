"""Tests for generation contribution registry."""

import pytest

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.generation_contribution_registry import (
    GenerationContributionRegistry,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


def test_registry_registers_generation_contribution() -> None:
    registry = GenerationContributionRegistry()

    preset = GenerationPresetId(
        GenerationPreset.COMPLETE.value,
    )

    contribution = GenerationContribution(
        id=PluginContributionId(
            "familyos.test.generation.complete",
        ),
        preset=preset,
        description="Complete package.",
        recipes=(
            "full_domain_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.get(
        preset,
    ) == contribution


def test_registry_lists_registered_contributions() -> None:
    registry = GenerationContributionRegistry()

    contribution = GenerationContribution(
        id=PluginContributionId(
            "familyos.test.generation.minimal",
        ),
        preset=GenerationPresetId(
            GenerationPreset.MINIMAL.value,
        ),
        description="Minimal package.",
        recipes=(
            "domain_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.all() == (
        contribution,
    )


def test_registry_rejects_duplicate_preset() -> None:
    registry = GenerationContributionRegistry()

    contribution = GenerationContribution(
        id=PluginContributionId(
            "familyos.test.generation.standard",
        ),
        preset=GenerationPresetId(
            GenerationPreset.STANDARD.value,
        ),
        description="Standard package.",
        recipes=(
            "domain_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            contribution,
        )
