from familyos_cli.domain.generation.domain_generator import (
    DomainGenerator,
)
from familyos_cli.domain.models.domain_artifact import (
    DomainArtifact,
)


def test_should_generate_domain_context() -> None:
    """Domain context should be generated."""

    artifact = DomainArtifact(
        name="Person",
        description="Person domain",
    )

    generator = DomainGenerator()

    context = generator.generate(
        artifact,
    )

    assert context.name == "Person"
    assert context.slug == "person"
    assert context.namespace == "person"
    assert context.title == "Person"
    assert context.description == "Person domain"


def test_should_return_domain_directories() -> None:
    """Domain directories should be generated."""

    artifact = DomainArtifact(
        name="Person",
    )

    generator = DomainGenerator()

    directories = generator.directories(
        artifact,
    )

    assert len(directories) == 7

    assert directories[0].as_posix() == ("docs/30-domains/person")


def test_should_return_domain_templates() -> None:
    """Domain templates should be generated."""

    generator = DomainGenerator()

    assert generator.templates() == (
        "README.md.j2",
        "Vision.md.j2",
        "API.md.j2",
        "Business-Rules.md.j2",
        "Capabilities.md.j2",
        "Domain-Model.md.j2",
        "Use-Cases.md.j2",
        "Security.md.j2",
    )
