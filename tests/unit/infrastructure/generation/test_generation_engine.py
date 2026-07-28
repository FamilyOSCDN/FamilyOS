from pathlib import Path

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


def test_generate_project(
    tmp_path: Path,
) -> None:
    """Generate a complete project."""

    engine = GenerationEngine()

    specification = GenerationSpecification(
        artifacts=[
            GenerationArtifact(
                template="project/README.md.j2",
                destination="README.md",
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

    assert (tmp_path / "README.md").exists()
