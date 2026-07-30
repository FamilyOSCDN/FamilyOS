"""Default generation catalog."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_catalog import (
    GenerationCatalog,
)
from familyos_cli.domain.generation.generation_catalog_entry import (
    GenerationCatalogEntry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_registry import (
    GenerationPresetRegistry,
)


class DefaultGenerationCatalog:
    """Create the default generation catalog."""

    @staticmethod
    def create(
        preset_registry: GenerationPresetRegistry,
    ) -> GenerationCatalog:
        """Create catalog from registered presets."""

        catalog = GenerationCatalog()

        catalog.register(
            GenerationCatalogEntry(
                preset=GenerationPreset.MINIMAL,
                description=(
                    "Minimal domain documentation package."
                ),
                recipes=(
                    "domain_documentation",
                ),
            ),
        )

        catalog.register(
            GenerationCatalogEntry(
                preset=GenerationPreset.STANDARD,
                description=(
                    "Standard domain documentation package."
                ),
                recipes=(
                    "domain_documentation",
                    "entity_documentation",
                    "aggregate_documentation",
                ),
            ),
        )

        catalog.register(
            GenerationCatalogEntry(
                preset=GenerationPreset.COMPLETE,
                description=(
                    "Complete domain documentation package."
                ),
                recipes=(
                    "full_domain_documentation",
                ),
            ),
        )

        return catalog
