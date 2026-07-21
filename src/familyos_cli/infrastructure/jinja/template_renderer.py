"""Jinja template renderer."""

from jinja2 import Environment, FileSystemLoader

from familyos_cli.infrastructure.jinja.template_context import (
    TemplateContext,
)


class TemplateRenderer:
    """Render Jinja templates."""

    def __init__(self) -> None:
        """Initialize the renderer."""

        self._environment = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        self._context = TemplateContext()

    def render(
        self,
        template: str,
        context: dict[str, object],
    ) -> str:
        """Render a template."""

        return self._environment.get_template(
            template,
        ).render(
            self._context.build(context),
        )