from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from familyos_cli.interfaces.cli.app import app

runner = CliRunner()


def test_cli_init_should_create_project(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        [
            "init",
            "DemoFamily",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0

    project = tmp_path / "DemoFamily"

    assert project.exists()
    assert project.is_dir()

    assert (project / "docs").exists()
    assert (project / "src").exists()
    assert (project / "tests").exists()
    assert (project / "scripts").exists()