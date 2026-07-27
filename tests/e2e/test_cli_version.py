"""End-to-end test for the version command."""

from typer.testing import CliRunner

from familyos_cli.main import app


runner = CliRunner()


def test_cli_should_display_version() -> None:
    result = runner.invoke(
        app,
        ["version"],
    )

    assert result.exit_code == 0
    assert "FamilyOS CLI v0.1.0" in result.stdout