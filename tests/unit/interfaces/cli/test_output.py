"""Tests for CLI output."""

from unittest.mock import Mock, patch

from familyos_cli.interfaces.cli.output import Output


@patch("typer.secho")
def test_success(mock_secho: Mock) -> None:
    """Success messages should be displayed."""

    Output.success("Done")

    mock_secho.assert_called_once_with(
        "✅ Done",
        fg="green",
    )


@patch("typer.secho")
def test_error(mock_secho: Mock) -> None:
    """Error messages should be displayed."""

    Output.error("Failed")

    mock_secho.assert_called_once_with(
        "❌ Failed",
        fg="red",
        err=True,
    )


@patch("typer.secho")
def test_warning(mock_secho: Mock) -> None:
    """Warning messages should be displayed."""

    Output.warning("Careful")

    mock_secho.assert_called_once_with(
        "⚠️ Careful",
        fg="yellow",
    )


@patch("typer.secho")
def test_info(mock_secho: Mock) -> None:
    """Information messages should be displayed."""

    Output.info("Hello")

    mock_secho.assert_called_once_with(
        "ℹ️ Hello",
        fg="blue",
    )
