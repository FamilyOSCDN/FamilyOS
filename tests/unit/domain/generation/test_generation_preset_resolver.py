from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.generation_preset import (
    GenerationPreset,
)
from familyos_cli.domain.generation.generation_preset_resolver import (
    GenerationPresetResolver,
)


def test_generation_preset_resolver_returns_definition() -> None:
    resolver = GenerationPresetResolver(
        DefaultGenerationPresetRegistry.create(),
    )

    definition = resolver.resolve(
        GenerationPreset.COMPLETE,
    )

    assert definition.preset is (
        GenerationPreset.COMPLETE
    )

    assert definition.recipes == (
        "full_domain_documentation",
    )
