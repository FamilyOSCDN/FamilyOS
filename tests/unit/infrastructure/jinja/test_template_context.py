"""Tests for the template renderer."""

from familyos_cli.infrastructure.jinja.template_renderer import (
    TemplateRenderer,
)


def test_renderer_should_inject_global_context() -> None:
    """Renderer should inject TemplateContext variables."""

    renderer = TemplateRenderer()

    content = renderer.render(
        "project/README.md.j2",
        {
            "project_name": "Demo",
        },
    )

    assert isinstance(content, str)