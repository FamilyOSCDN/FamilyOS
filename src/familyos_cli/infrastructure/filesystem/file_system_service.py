"""Filesystem service."""

from pathlib import Path

from familyos_cli.shared.exceptions import (
    ProjectAlreadyExistsError,
)


class FileSystemService:
    """Provide filesystem operations."""

    def create_directory(self, path: Path) -> None:
        """Create a directory."""

        try:
            path.mkdir(parents=True, exist_ok=False)

        except FileExistsError as error:
            raise ProjectAlreadyExistsError(
                f'Project "{path.name}" already exists.'
            ) from error

    def write_text_file(
        self,
        path: Path,
        content: str,
    ) -> None:
        """Write a UTF-8 text file."""

        path.write_text(
            content,
            encoding="utf-8",
        )
