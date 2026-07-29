from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


def test_complete_preset_contains_full_domain_documentation() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    definition = registry.get(
        GenerationPreset.COMPLETE,
    )

    assert (
        "full_domain_documentation"
        in definition.recipes
    )


def test_all_presets_have_at_least_one_recipe() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    for preset in GenerationPreset:
        definition = registry.get(
            preset,
        )

        assert definition.recipes
