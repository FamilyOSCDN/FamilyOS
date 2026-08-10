"""Tests for generation contributions."""

import pytest

from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


def test_generation_contribution_creation() -> None:
    """Generation contribution should preserve its configuration."""

    contribution = GenerationContribution(
        id=PluginContributionId(
            "familyos.test.generation",
        ),
        preset=GenerationPreset.COMPLETE,
        description="Complete generation package.",
        recipes=(
            "full_domain_documentation",
        ),
    )

    assert contribution.id == PluginContributionId(
        "familyos.test.generation",
    )

    assert contribution.preset == (
        GenerationPreset.COMPLETE
    )

    assert contribution.description == (
        "Complete generation package."
    )

    assert contribution.recipes == (
        "full_domain_documentation",
    )


def test_generation_contribution_is_immutable() -> None:
    """Generation contributions should be immutable."""

    contribution = GenerationContribution(
        id=PluginContributionId(
            "familyos.test.generation",
        ),
        preset=GenerationPreset.MINIMAL,
        description="Minimal package.",
        recipes=(
            "domain_documentation",
        ),
    )

    with pytest.raises(
        AttributeError,
    ):
        contribution.description = "Changed"
