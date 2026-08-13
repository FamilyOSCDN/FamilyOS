import pytest

from familyos_cli.domain.generation.generation_catalog import (
    GenerationCatalog,
)
from familyos_cli.domain.generation.generation_catalog_entry import (
    GenerationCatalogEntry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


def test_generation_catalog_registers_and_returns_entry() -> None:
    catalog = GenerationCatalog()

    preset = GenerationPresetId(
        GenerationPreset.COMPLETE.value,
    )

    entry = GenerationCatalogEntry(
        preset=preset,
        description="Complete domain documentation package.",
        recipes=(
            "full_domain_documentation",
        ),
    )

    catalog.register(
        entry,
    )

    result = catalog.get(
        preset,
    )

    assert result == entry


def test_generation_catalog_lists_entries() -> None:
    catalog = GenerationCatalog()

    catalog.register(
        GenerationCatalogEntry(
            preset=GenerationPresetId(
                GenerationPreset.MINIMAL.value,
            ),
            description="Minimal documentation package.",
            recipes=(
                "domain_documentation",
            ),
        ),
    )

    catalog.register(
        GenerationCatalogEntry(
            preset=GenerationPresetId(
                GenerationPreset.STANDARD.value,
            ),
            description="Standard domain documentation package.",
            recipes=(
                "domain_documentation",
                "entity_documentation",
            ),
        ),
    )

    entries = catalog.list()

    assert len(entries) == 2


def test_generation_catalog_rejects_duplicate_preset() -> None:
    catalog = GenerationCatalog()

    entry = GenerationCatalogEntry(
        preset=GenerationPresetId(
            GenerationPreset.MINIMAL.value,
        ),
        description="Minimal documentation package.",
        recipes=(
            "domain_documentation",
        ),
    )

    catalog.register(
        entry,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        catalog.register(
            entry,
        )
