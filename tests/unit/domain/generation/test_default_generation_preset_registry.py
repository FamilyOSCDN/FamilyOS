from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


def test_default_generation_preset_registry_creates_presets() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    presets = registry.list()

    assert len(presets) == 3

    assert [
        preset.preset
        for preset in presets
    ] == [
        GenerationPreset.MINIMAL,
        GenerationPreset.STANDARD,
        GenerationPreset.COMPLETE,
    ]


def test_complete_preset_contains_full_domain_documentation() -> None:
    registry = DefaultGenerationPresetRegistry.create()

    preset = registry.get(
        GenerationPreset.COMPLETE,
    )

    assert preset.recipes == (
        "full_domain_documentation",
    )
