"""File generator."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.infrastructure.jinja.template_renderer import (
    TemplateRenderer,
)


class FileGenerator:
    """Generate project files."""

    def __init__(
        self,
        template_directories: tuple[Path, ...] = (
            Path("templates"),
        ),
    ) -> None:
        """Initialize the file generator."""

        self._template_directories = template_directories

        self._renderer = TemplateRenderer(
            template_directories=template_directories,
        )

    @property
    def template_directories(
        self,
    ) -> tuple[Path, ...]:
        """Return the configured template directories."""

        return self._template_directories

    def generate(
        self,
        destination: Path,
        files: list[ProjectFile],
        context: dict[str, object],
    ) -> None:
        """Generate project files."""

        for project_file in files:
            output = destination / project_file.path

            output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_context = {
                **context,
                **project_file.context,
            }

            output.write_text(
                self._renderer.render(
                    template=project_file.template,
                    context=file_context,
                ),
                encoding="utf-8",
            )
