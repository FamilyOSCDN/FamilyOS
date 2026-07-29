from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_definition import (
    GenerationPresetDefinition,
)


def test_generation_preset_definition_creation() -> None:
    definition = GenerationPresetDefinition(
        preset=GenerationPreset.COMPLETE,
        recipes=(
            "full_domain_documentation",
        ),
    )

    assert (
        definition.preset
        is GenerationPreset.COMPLETE
    )

    assert definition.recipes == (
        "full_domain_documentation",
    )
