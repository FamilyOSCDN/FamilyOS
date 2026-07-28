from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


def test_generation_request_creation() -> None:
    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
        profile=GenerationProfile.DOMAIN_DOCUMENTATION,
    )

    assert request.domain_name == "Person"

    assert request.recipe_name == (
        "domain_documentation"
    )

    assert request.profile == (
        GenerationProfile.DOMAIN_DOCUMENTATION
    )


def test_generation_request_default_profile() -> None:
    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    assert request.profile == (
        GenerationProfile.PYTHON_IMPLEMENTATION
    )


def test_generation_request_is_immutable() -> None:
    request = GenerationRequest(
        domain_name="Person",
        recipe_name="domain_documentation",
    )

    try:
        request.domain_name = "Family"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "Expected AttributeError.",
        )
