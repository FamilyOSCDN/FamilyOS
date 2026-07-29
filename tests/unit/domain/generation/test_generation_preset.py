from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


def test_generation_presets_exist() -> None:
    assert (
        GenerationPreset.MINIMAL.value
        == "minimal"
    )

    assert (
        GenerationPreset.STANDARD.value
        == "standard"
    )

    assert (
        GenerationPreset.COMPLETE.value
        == "complete"
    )
