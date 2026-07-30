"""Generation catalog service."""

from __future__ import annotations

from familyos_cli.application.generation.plugin_generation_catalog_contributor import (
    PluginGenerationCatalogContributor,
)
from familyos_cli.domain.generation.default_generation_catalog import (
    DefaultGenerationCatalog,
)
from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_catalog import (
    GenerationCatalog,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)


class GenerationCatalogService:
    """Provide access to generation catalog information."""

    def __init__(
        self,
        generation_contributions: tuple[
            GenerationContribution,
            ...
        ] = (),
    ) -> None:
        """Initialize the service."""

        self._catalog = (
            DefaultGenerationCatalog.create(
                DefaultGenerationPresetRegistry.create(),
            )
        )

        PluginGenerationCatalogContributor().contribute(
            self._catalog,
            generation_contributions,
        )

    def get_catalog(
        self,
    ) -> GenerationCatalog:
        """Return the generation catalog."""

        return self._catalog
