from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_definition import (
    GenerationPresetDefinition,
)
from familyos_cli.domain.generation.generation_preset_registry import (
    GenerationPresetRegistry,
)


def test_generation_preset_registry_registers_and_returns_preset() -> None:
    registry = GenerationPresetRegistry()

    definition = GenerationPresetDefinition(
        preset=GenerationPreset.COMPLETE,
        recipes=(
            "full_domain_documentation",
        ),
    )

    registry.register(
        definition,
    )

    assert (
        registry.get(
            GenerationPreset.COMPLETE,
        )
        == definition
    )


def test_generation_preset_registry_lists_presets() -> None:
    registry = GenerationPresetRegistry()

    registry.register(
        GenerationPresetDefinition(
            preset=GenerationPreset.MINIMAL,
            recipes=(
                "domain_documentation",
            ),
        ),
    )

    assert len(
        registry.list(),
    ) == 1
