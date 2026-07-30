from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)


def test_generation_contribution_creation() -> None:
    contribution = GenerationContribution(
        preset=GenerationPreset.COMPLETE,
        description="Complete generation package.",
        recipes=(
            "full_domain_documentation",
        ),
    )

    assert contribution.preset == (
        GenerationPreset.COMPLETE
    )

    assert contribution.description == (
        "Complete generation package."
    )

    assert (
        "full_domain_documentation"
        in contribution.recipes
    )


def test_generation_contribution_is_immutable() -> None:
    contribution = GenerationContribution(
        preset=GenerationPreset.MINIMAL,
        description="Minimal package.",
        recipes=(
            "domain_documentation",
        ),
    )

    assert contribution.recipes == (
        "domain_documentation",
    )
