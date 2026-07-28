"""Tests for TemplateRenderer."""

from pathlib import Path

from familyos_cli.infrastructure.jinja.template_renderer import (
    TemplateRenderer,
)


def test_should_store_template_directories() -> None:
    """TemplateRenderer should expose template directories."""

    renderer = TemplateRenderer(
        template_directories=(
            Path("templates"),
            Path("plugins/blog/templates"),
        ),
    )

    assert renderer.template_directories == (
        Path("templates"),
        Path("plugins/blog/templates"),
    )
