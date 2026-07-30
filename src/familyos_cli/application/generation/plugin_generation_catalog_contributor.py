"""Plugin generation catalog contributor."""

from __future__ import annotations

from familyos_cli.domain.generation.generation_catalog import (
    GenerationCatalog,
)
from familyos_cli.domain.generation.generation_catalog_entry import (
    GenerationCatalogEntry,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)


class PluginGenerationCatalogContributor:
    """Add plugin generation contributions to a catalog."""

    def contribute(
        self,
        catalog: GenerationCatalog,
        contributions: tuple[
            GenerationContribution,
            ...,
        ],
    ) -> None:
        """Register plugin contributions in catalog."""

        for contribution in contributions:
            catalog.register(
                GenerationCatalogEntry(
                    preset=contribution.preset,
                    description=contribution.description,
                    recipes=contribution.recipes,
                ),
            )
