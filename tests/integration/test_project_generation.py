"""Integration tests for project generation."""

from pathlib import Path

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)


def test_create_project(tmp_path: Path, monkeypatch) -> None:
    """Generate a complete project."""

    monkeypatch.chdir(tmp_path)

    (tmp_path / "specifications").mkdir()
    (tmp_path / "templates").mkdir()
    (tmp_path / "templates" / "project").mkdir()

    (tmp_path / "specifications" / "project.yaml").write_text(
        """
version: 1

project:
  directories:
    - docs
    - src
    - tests
    - scripts

  files:
    - destination: README.md
      template: project/README.md.j2
""",
        encoding="utf-8",
    )

    (tmp_path / "templates" / "project" / "README.md.j2").write_text(
        "# {{ project_name }}\n",
        encoding="utf-8",
    )

    CreateProjectUseCase().execute("demo")

    project = tmp_path / "demo"

    assert project.exists()

    assert (project / "docs").is_dir()
    assert (project / "src").is_dir()
    assert (project / "tests").is_dir()
    assert (project / "scripts").is_dir()

    readme = project / "README.md"

    assert readme.exists()
    assert readme.read_text(encoding="utf-8") == "# demo"