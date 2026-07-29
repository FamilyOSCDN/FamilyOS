from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
)
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
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


def create_factory() -> GenerationRequestFactory:
    """Create factory with preset support."""

    return GenerationRequestFactory(
        PresetRecipeResolver(
            GenerationPresetResolver(
                DefaultGenerationPresetRegistry.create(),
            ),
        ),
    )


def test_generation_request_factory_creates_default_request() -> None:
    factory = GenerationRequestFactory()

    request = factory.create(
        "Person",
    )

    assert isinstance(
        request,
        GenerationRequest,
    )

    assert request.domain_name == "Person"

    assert request.recipe_name == (
        "domain_documentation"
    )


def test_generation_request_factory_accepts_custom_recipe() -> None:
    factory = GenerationRequestFactory()

    request = factory.create(
        domain_name="Person",
        recipe_name="custom_recipe",
    )

    assert request.recipe_name == (
        "custom_recipe"
    )


def test_generation_request_factory_resolves_preset() -> None:
    factory = create_factory()

    request = factory.create(
        domain_name="Person",
        preset=GenerationPreset.COMPLETE,
    )

    assert request.recipe_name == (
        "full_domain_documentation"
    )
