"""Filesystem service."""

from pathlib import Path


class FileSystemService:
    """Provide filesystem operations."""

    def create_directory(self, path: Path) -> None:
        """Create a directory."""
        path.mkdir(parents=True, exist_ok=False)

    def write_text_file(
        self,
        path: Path,
        content: str,
    ) -> None:
        """Write a UTF-8 text file."""
        path.write_text(content, encoding="utf-8")