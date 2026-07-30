"""Generation catalog service."""

from __future__ import annotations

from familyos_cli.domain.generation.default_generation_catalog import (
    DefaultGenerationCatalog,
)
from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_catalog import (
    GenerationCatalog,
)


class GenerationCatalogService:
    """Provide access to generation catalog information."""

    def __init__(
        self,
    ) -> None:
        """Initialize the service."""

        self._catalog = (
            DefaultGenerationCatalog.create(
                DefaultGenerationPresetRegistry.create(),
            )
        )

    def get_catalog(
        self,
    ) -> GenerationCatalog:
        """Return the generation catalog."""

        return self._catalog
