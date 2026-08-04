from pathlib import Path

TEMPLATE_ROOT = (
    Path(__file__)
    .parents[6]
    / "src"
    / "familyos_cli"
    / "plugins"
    / "builtin"
    / "documents"
    / "templates"
)


def test_documents_templates_exist() -> None:
    templates = [
        (
            "documentation",
            "documents_documentation.md.j2",
        ),
        (
            "capabilities",
            "documents_capabilities.md.j2",
        ),
    ]

    for directory, filename in templates:
        assert (
            TEMPLATE_ROOT
            / directory
            / filename
        ).exists()


def test_documents_templates_are_not_empty() -> None:
    templates = [
        (
            TEMPLATE_ROOT
            / "documentation"
            / "documents_documentation.md.j2"
        ),
        (
            TEMPLATE_ROOT
            / "capabilities"
            / "documents_capabilities.md.j2"
        ),
    ]

    for template in templates:
        assert template.read_text(
            encoding="utf-8",
        ).strip()


def test_documents_templates_use_domain_name() -> None:
    templates = [
        (
            TEMPLATE_ROOT
            / "documentation"
            / "documents_documentation.md.j2"
        ),
        (
            TEMPLATE_ROOT
            / "capabilities"
            / "documents_capabilities.md.j2"
        ),
    ]

    for template in templates:
        content = template.read_text(
            encoding="utf-8",
        )

        assert "{{ domain_name }}" in content
