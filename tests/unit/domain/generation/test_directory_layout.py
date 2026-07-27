from pathlib import Path

from familyos_cli.domain.generation.directory_layout import (
    DirectoryLayout,
)


def test_should_return_domain_root() -> None:
    """Domain root should be generated."""

    layout = DirectoryLayout()

    assert layout.root("Person") == Path(
        "docs/30-domains/person",
    )


def test_should_return_all_directories() -> None:
    """All directories should be generated."""

    layout = DirectoryLayout()

    assert layout.directories("Person") == (
        Path("docs/30-domains/person"),
        Path("docs/30-domains/person/aggregates"),
        Path("docs/30-domains/person/entities"),
        Path("docs/30-domains/person/value-objects"),
        Path("docs/30-domains/person/repositories"),
        Path("docs/30-domains/person/services"),
        Path("docs/30-domains/person/diagrams"),
    )


def test_should_return_document_files() -> None:
    """Documentation files should be generated."""

    layout = DirectoryLayout()

    assert layout.documents("Person") == (
        Path("docs/30-domains/person/README.md"),
        Path("docs/30-domains/person/Vision.md"),
        Path("docs/30-domains/person/API.md"),
        Path("docs/30-domains/person/Business-Rules.md"),
        Path("docs/30-domains/person/Capabilities.md"),
        Path("docs/30-domains/person/Domain-Model.md"),
        Path("docs/30-domains/person/Use-Cases.md"),
        Path("docs/30-domains/person/Security.md"),
    )