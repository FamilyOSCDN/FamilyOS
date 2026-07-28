"""Tests for FileGenerator template directories."""

from pathlib import Path

from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)


def test_should_store_template_directories() -> None:
    """FileGenerator should expose template directories."""

    generator = FileGenerator(
        template_directories=(
            Path("templates"),
            Path("plugins/blog/templates"),
        ),
    )

    assert generator.template_directories == (
        Path("templates"),
        Path("plugins/blog/templates"),
    )
