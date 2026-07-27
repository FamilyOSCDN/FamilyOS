from familyos_cli.domain.generation.template_provider import (
    TemplateProvider,
)


def test_should_return_domain_templates() -> None:
    """Domain templates should be available."""

    provider = TemplateProvider()

    assert provider.templates() == (
        "README.md.j2",
        "Vision.md.j2",
        "API.md.j2",
        "Business-Rules.md.j2",
        "Capabilities.md.j2",
        "Domain-Model.md.j2",
        "Use-Cases.md.j2",
        "Security.md.j2",
    )