"""Tests for FileGenerator."""

from pathlib import Path

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)


def test_generate_file(tmp_path: Path) -> None:
    """Generate a file from a template."""

    generator = FileGenerator()

    generator.generate(
        destination=tmp_path,
        files=[
            ProjectFile(
                destination="README.md",
                template="project/README.md.j2",
            ),
        ],
        context={
            "project_name": "Demo",
        },
    )

    readme = tmp_path / "README.md"

    assert readme.exists()
    assert readme.is_file()

    content = readme.read_text(encoding="utf-8")

    assert "Demo" in content