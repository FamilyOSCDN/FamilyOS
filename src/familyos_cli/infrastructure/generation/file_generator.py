"""File generator."""

from pathlib import Path

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.infrastructure.filesystem.file_system_service import (
    FileSystemService,
)
from familyos_cli.infrastructure.jinja.template_renderer import (
    TemplateRenderer,
)


class FileGenerator:
    """Generate project files from templates."""

    def __init__(self) -> None:
        """Initialize the file generator."""
        self._filesystem = FileSystemService()
        self._renderer = TemplateRenderer()

    def generate(
        self,
        destination: Path,
        files: list[ProjectFile],
        context: dict[str, object],
    ) -> None:
        """Generate all project files."""

        for project_file in files:
            content = self._renderer.render(
                project_file.template,
                context,
            )

            self._filesystem.write_text_file(
                destination / project_file.destination,
                content,
            )