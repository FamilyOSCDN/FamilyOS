from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


def test_minimal_preset_contains_domain_documentation() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    definition = registry.get(
        GenerationPreset.MINIMAL,
    )

    assert definition.recipes == (
        "domain_documentation",
    )


def test_standard_preset_contains_domain_model_recipes() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    definition = registry.get(
        GenerationPreset.STANDARD,
    )

    assert definition.recipes == (
        "domain_documentation",
        "entity_documentation",
        "aggregate_documentation",
    )


def test_complete_preset_contains_full_domain_documentation() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    definition = registry.get(
        GenerationPreset.COMPLETE,
    )

    assert definition.recipes == (
        "full_domain_documentation",
    )


def test_all_presets_have_at_least_one_recipe() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    for preset in GenerationPreset:
        definition = registry.get(
            preset,
        )

        assert definition.recipes
