from familyos_cli.domain.generation.generation_profile import (
    GenerationProfile,
)


def test_generation_profiles_exist() -> None:
    assert (
        GenerationProfile.DOMAIN_DOCUMENTATION.value
        == "domain_documentation"
    )

    assert (
        GenerationProfile.PYTHON_IMPLEMENTATION.value
        == "python_implementation"
    )
