from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


def test_should_create_project() -> None:
    use_case = CreateProjectUseCase()

    with patch(
        "familyos_cli.application.use_cases.create_project.GenerationPipeline.run"
    ) as mock_run:
        use_case.execute(
            name="MyFamily",
            destination=Path("/tmp"),
        )

    mock_run.assert_called_once()

    context = mock_run.call_args.args[0]

    assert context.project.name == "MyFamily"
    assert context.destination == Path("/tmp")
    assert context.variables["project_name"] == "MyFamily"