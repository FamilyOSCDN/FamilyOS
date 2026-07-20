"""Directory generator."""

from pathlib import Path


class DirectoryGenerator:
    """Generate project directories."""

    def generate(
        self,
        destination: Path,
        directories: list[str],
    ) -> None:
        """Generate directories."""

        for directory in directories:
            (destination / directory).mkdir(
                parents=True,
                exist_ok=True,
            )