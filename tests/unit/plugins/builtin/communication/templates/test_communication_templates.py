"""Tests for Communication templates."""

from pathlib import Path

TEMPLATE_ROOT = (
    Path(__file__)
    .parents[6]
    / "src"
    / "familyos_cli"
    / "plugins"
    / "builtin"
    / "communication"
    / "templates"
)


def test_communication_templates_exist() -> None:
    templates = [
        (
            "documentation",
            "communication_documentation.md.j2",
        ),
        (
            "capabilities",
            "communication_capabilities.md.j2",
        ),
    ]

    for directory, filename in templates:
        assert (
            TEMPLATE_ROOT
            / directory
            / filename
        ).exists()


def test_communication_templates_are_not_empty() -> None:
    templates = [
        (
            TEMPLATE_ROOT
            / "documentation"
            / "communication_documentation.md.j2"
        ),
        (
            TEMPLATE_ROOT
            / "capabilities"
            / "communication_capabilities.md.j2"
        ),
    ]

    for template in templates:
        assert template.read_text(
            encoding="utf-8",
        ).strip()


def test_communication_templates_use_domain_name() -> None:
    templates = [
        (
            TEMPLATE_ROOT
            / "documentation"
            / "communication_documentation.md.j2"
        ),
        (
            TEMPLATE_ROOT
            / "capabilities"
            / "communication_capabilities.md.j2"
        ),
    ]

    for template in templates:
        content = template.read_text(
            encoding="utf-8",
        )

        assert "{{ domain_name }}" in content
