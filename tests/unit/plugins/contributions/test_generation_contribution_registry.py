from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.generation_contribution_registry import (
    GenerationContributionRegistry,
)


def test_registry_registers_generation_contribution() -> None:
    registry = GenerationContributionRegistry()

    contribution = GenerationContribution(
        preset=GenerationPreset.COMPLETE,
        description="Complete package.",
        recipes=(
            "full_domain_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    result = registry.get(
        GenerationPreset.COMPLETE,
    )

    assert result == contribution


def test_registry_lists_registered_contributions() -> None:
    registry = GenerationContributionRegistry()

    contribution = GenerationContribution(
        preset=GenerationPreset.MINIMAL,
        description="Minimal package.",
        recipes=(
            "domain_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    assert registry.list() == (
        contribution,
    )


def test_registry_rejects_duplicate_preset() -> None:
    registry = GenerationContributionRegistry()

    contribution = GenerationContribution(
        preset=GenerationPreset.STANDARD,
        description="Standard package.",
        recipes=(
            "domain_documentation",
        ),
    )

    registry.register(
        contribution,
    )

    try:
        registry.register(
            contribution,
        )

        raise AssertionError(
            "Expected duplicate contribution error.",
        )

    except ValueError:
        pass
