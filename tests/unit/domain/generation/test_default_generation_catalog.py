from familyos_cli.domain.generation.default_generation_catalog import (
    DefaultGenerationCatalog,
)
from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


def test_default_generation_catalog_contains_all_presets() -> None:
    preset_registry = (
        DefaultGenerationPresetRegistry.create()
    )

    catalog = DefaultGenerationCatalog.create(
        preset_registry,
    )

    entries = catalog.list()

    assert len(entries) == 3


def test_complete_catalog_entry_contains_full_documentation_recipe() -> None:
    preset_registry = (
        DefaultGenerationPresetRegistry.create()
    )

    catalog = DefaultGenerationCatalog.create(
        preset_registry,
    )

    entry = catalog.get(
        GenerationPreset.COMPLETE,
    )

    assert (
        "full_domain_documentation"
        in entry.recipes
    )


def test_default_generation_catalog_entries_have_descriptions() -> None:
    preset_registry = (
        DefaultGenerationPresetRegistry.create()
    )

    catalog = DefaultGenerationCatalog.create(
        preset_registry,
    )

    for entry in catalog.list():
        assert entry.description
        assert entry.recipes
