"""Jinja template renderer."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateRenderer:
    """Render Jinja templates."""

    def __init__(
        self,
        template_directories: tuple[Path, ...] | None = None,
    ) -> None:
        """Initialize the template renderer."""

        if template_directories is None:
            template_root = (
                Path(__file__)
                .resolve()
                .parents[4]
                / "templates"
            )

            template_directories = (
                template_root,
            )

        self._template_directories = template_directories

        self._environment = Environment(
            loader=FileSystemLoader(
                [
                    str(directory)
                    for directory in template_directories
                ],
            ),
            undefined=StrictUndefined,
        )

    @property
    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return the template directories."""

        return self._template_directories

    def render(
        self,
        template: str,
        context: dict[str, object],
    ) -> str:
        """Render a template."""

        return self._environment.get_template(
            template,
        ).render(
            **context,
        )