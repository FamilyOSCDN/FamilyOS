from familyos_cli.application.generation.plugin_generation_catalog_contributor import (
    PluginGenerationCatalogContributor,
)
from familyos_cli.domain.generation.generation_catalog import (
    GenerationCatalog,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.plugins.contributions.generation_contribution import (
    GenerationContribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)


def test_plugin_generation_contribution_is_added_to_catalog() -> None:
    catalog = GenerationCatalog()

    contributor = PluginGenerationCatalogContributor()

    preset = GenerationPresetId(
        GenerationPreset.COMPLETE.value,
    )

    contribution = GenerationContribution(
        id=PluginContributionId(
            "familyos.test.generation.complete",
        ),
        preset=preset,
        description="Security documentation package.",
        recipes=(
            "security_documentation",
        ),
    )

    contributor.contribute(
        catalog,
        (
            contribution,
        ),
    )

    entry = catalog.get(
        preset,
    )

    assert entry.description == (
        "Security documentation package."
    )

    assert (
        "security_documentation"
        in entry.recipes
    )


def test_multiple_plugin_generation_contributions_are_added() -> None:
    catalog = GenerationCatalog()

    contributor = PluginGenerationCatalogContributor()

    contributor.contribute(
        catalog,
        (
            GenerationContribution(
                id=PluginContributionId(
                    "familyos.test.generation.minimal",
                ),
                preset=GenerationPresetId(
                    GenerationPreset.MINIMAL.value,
                ),
                description="Minimal package.",
                recipes=(
                    "minimal_documentation",
                ),
            ),
            GenerationContribution(
                id=PluginContributionId(
                    "familyos.test.generation.standard",
                ),
                preset=GenerationPresetId(
                    GenerationPreset.STANDARD.value,
                ),
                description="Standard package.",
                recipes=(
                    "standard_documentation",
                ),
            ),
        ),
    )

    assert len(catalog.list()) == 2
