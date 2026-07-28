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

        default_template_directory = (
            Path(__file__).resolve().parents[4]
            / "templates"
        )

        if template_directories is None:
            template_directories = (
                default_template_directory,
            )

        self._template_directories = template_directories

        search_directories = list(
            template_directories,
        )

        default_resolved = (
            default_template_directory.resolve()
        )

        if all(
            directory.resolve() != default_resolved
            for directory in search_directories
        ):
            search_directories.append(
                default_template_directory,
            )

        self._environment = Environment(
            loader=FileSystemLoader(
                [
                    str(directory)
                    for directory in search_directories
                ],
            ),
            undefined=StrictUndefined,
        )

    @property
    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return the configured template directories."""

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
