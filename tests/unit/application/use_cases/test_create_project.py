from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

from familyos_cli.application.generation.generation_pipeline import (
    GenerationPipeline,
)
from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


def test_should_create_project() -> None:
    """Create a project through the generation pipeline."""

    pipeline = Mock(spec=GenerationPipeline)

    use_case = CreateProjectUseCase(
        pipeline=pipeline,
    )

    use_case.execute(
        name="MyFamily",
        destination=Path("/tmp"),
    )

    pipeline.run.assert_called_once()

    context = pipeline.run.call_args.args[0]

    assert context.project.name == "MyFamily"
    assert context.destination == Path("/tmp")
    assert context.variables["project_name"] == "MyFamily"