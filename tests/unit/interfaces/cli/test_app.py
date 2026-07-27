from __future__ import annotations

from typer.testing import CliRunner

from familyos_cli.interfaces.cli.app import app


runner = CliRunner()


def test_should_display_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "FamilyOS CLI" in result.stdout