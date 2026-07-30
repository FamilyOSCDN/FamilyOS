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


def test_generation_catalog_registers_and_returns_entry() -> None:
    catalog = GenerationCatalog()

    entry = GenerationCatalogEntry(
        preset=GenerationPreset.COMPLETE,
        description="Complete domain documentation package.",
        recipes=(
            "full_domain_documentation",
        ),
    )

    catalog.register(
        entry,
    )

    result = catalog.get(
        GenerationPreset.COMPLETE,
    )

    assert result == entry


def test_generation_catalog_lists_entries() -> None:
    catalog = GenerationCatalog()

    catalog.register(
        GenerationCatalogEntry(
            preset=GenerationPreset.MINIMAL,
            description="Minimal documentation package.",
            recipes=(
                "domain_documentation",
            ),
        ),
    )

    catalog.register(
        GenerationCatalogEntry(
            preset=GenerationPreset.STANDARD,
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
        preset=GenerationPreset.MINIMAL,
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
