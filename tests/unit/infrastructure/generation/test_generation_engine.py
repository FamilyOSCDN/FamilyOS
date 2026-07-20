"""Tests for GenerationEngine."""

from pathlib import Path

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


def test_generate_project(tmp_path: Path) -> None:
    """Generate a complete project."""

    engine = GenerationEngine()

    specification = ProjectSpecification(
        directories=[
            "docs",
            "src",
            "tests",
        ],
        files=[
            ProjectFile(
                destination="README.md",
                template="project/README.md.j2",
            ),
        ],
    )

    engine.generate(
        destination=tmp_path,
        specification=specification,
        context={
            "project_name": "Demo",
        },
    )

    assert (tmp_path / "docs").is_dir()
    assert (tmp_path / "src").is_dir()
    assert (tmp_path / "tests").is_dir()

    readme = tmp_path / "README.md"

    assert readme.exists()
    assert "Demo" in readme.read_text(encoding="utf-8")