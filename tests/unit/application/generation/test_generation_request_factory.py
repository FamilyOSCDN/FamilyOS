from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
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
