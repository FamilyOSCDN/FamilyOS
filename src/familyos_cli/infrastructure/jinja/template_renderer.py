"""Template rendering using Jinja2."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    """Render Jinja2 templates."""

    def __init__(self) -> None:
        """Initialize the template renderer."""
        template_directory = Path("templates")

        self._environment = Environment(
            loader=FileSystemLoader(template_directory),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(
        self,
        template_name: str,
        context: dict[str, object],
    ) -> str:
        """Render a template with the provided context."""
        template = self._environment.get_template(template_name)
        return template.render(**context)