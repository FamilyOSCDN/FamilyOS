from __future__ import annotations

from pathlib import Path

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


def test_should_create_project(tmp_path: Path) -> None:
    use_case = CreateProjectUseCase()

    use_case.execute(
        name="DemoFamily",
        destination=tmp_path,
    )

    project = tmp_path / "DemoFamily"

    assert project.exists()