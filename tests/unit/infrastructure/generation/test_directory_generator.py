"""Tests for DirectoryGenerator."""

from pathlib import Path

from familyos_cli.infrastructure.generation.directory_generator import (
    DirectoryGenerator,
)


def test_generate_directories(tmp_path: Path) -> None:
    """Generate directories from a specification."""

    generator = DirectoryGenerator()

    generator.generate(
        destination=tmp_path,
        directories=[
            "docs",
            "src",
            "tests",
            "scripts",
        ],
    )

    assert (tmp_path / "docs").is_dir()
    assert (tmp_path / "src").is_dir()
    assert (tmp_path / "tests").is_dir()
    assert (tmp_path / "scripts").is_dir()
