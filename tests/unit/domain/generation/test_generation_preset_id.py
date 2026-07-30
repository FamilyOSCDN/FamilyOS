from pytest import raises

from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


def test_generation_preset_id_creation() -> None:
    preset = GenerationPresetId(
        "security",
    )

    assert preset.value == "security"


def test_generation_preset_id_string_representation() -> None:
    preset = GenerationPresetId(
        "security",
    )

    assert str(preset) == "security"


def test_generation_preset_id_rejects_empty_value() -> None:
    with raises(ValueError):
        GenerationPresetId("")
