from familyos_cli.application.generation.preset_recipe_resolver import (
    PresetRecipeResolver,
)
from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_resolver import (
    GenerationPresetResolver,
)


def test_preset_recipe_resolver_returns_recipe_name() -> None:
    resolver = PresetRecipeResolver(
        GenerationPresetResolver(
            DefaultGenerationPresetRegistry.create(),
        ),
    )

    recipe = resolver.resolve(
        GenerationPreset.COMPLETE,
    )

    assert recipe == "full_domain_documentation"
