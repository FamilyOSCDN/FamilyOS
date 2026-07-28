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
                path="README.md",
                template="project/README.md.j2",
            ),
        ],
        context={
            "project_name": "Demo",
        },
    )

    assert (tmp_path / "README.md").exists()
