from familyos_cli.application.generation.generation_catalog_service import (
    GenerationCatalogService,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)


def test_generation_catalog_service_returns_catalog() -> None:
    service = GenerationCatalogService()

    catalog = service.get_catalog()

    entry = catalog.get(
        GenerationPreset.COMPLETE,
    )

    assert entry.preset == (
        GenerationPreset.COMPLETE
    )


def test_generation_catalog_service_exposes_all_presets() -> None:
    service = GenerationCatalogService()

    catalog = service.get_catalog()

    entries = catalog.list()

    assert len(entries) == 3
