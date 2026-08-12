"""Tests for diagnostic CLI output."""

from unittest.mock import patch

from _pytest.capture import CaptureFixture

from familyos_cli.interfaces.cli.output import Output


def test_diagnostic_writes_unmodified_message_to_stderr(
    capsys: CaptureFixture[str],
) -> None:
    """Rendered diagnostics are written to stderr without a prefix."""

    Output.diagnostic(
        "ERROR: Missing plugin dependency",
    )

    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == (
        "ERROR: Missing plugin dependency\n"
    )


def test_diagnostic_preserves_multiline_output(
    capsys: CaptureFixture[str],
) -> None:
    """Rendered diagnostic sections remain unchanged."""

    message = (
        "ERROR: Missing plugin dependency\n\n"
        "A required dependency is unavailable.\n\n"
        "Causes:\n"
        "- security requires crypto\n\n"
        "Suggestions:\n"
        "- Install the missing plugin."
    )

    Output.diagnostic(message)

    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == f"{message}\n"


def test_diagnostic_does_not_add_generic_error_prefix(
    capsys: CaptureFixture[str],
) -> None:
    """Diagnostic output does not receive an additional error marker."""

    Output.diagnostic(
        "ERROR: Version conflict",
    )

    captured = capsys.readouterr()

    assert captured.out == ""
    assert "❌" not in captured.err
    assert captured.err == "ERROR: Version conflict\n"


@patch("typer.echo")
@patch("typer.secho")
def test_styled_diagnostic_styles_only_heading(
    mock_secho,
    mock_echo,
) -> None:
    """Styled diagnostics should keep body text separate from styling."""

    message = (
        "ERROR: Missing plugin dependency\n\n"
        "A required dependency is unavailable.\n\n"
        "Suggestions:\n"
        "- Install the missing plugin."
    )

    Output.diagnostic(
        message,
        styled=True,
    )

    mock_secho.assert_called_once_with(
        "ERROR: Missing plugin dependency",
        fg="red",
        bold=True,
        err=True,
    )

    mock_echo.assert_called_once_with(
        (
            "\n"
            "A required dependency is unavailable.\n\n"
            "Suggestions:\n"
            "- Install the missing plugin."
        ),
        err=True,
    )


@patch("typer.echo")
@patch("typer.secho")
def test_styled_single_line_diagnostic_does_not_emit_empty_body(
    mock_secho,
    mock_echo,
) -> None:
    """Single-line styled diagnostics should not emit an extra body."""

    Output.diagnostic(
        "ERROR: Version conflict",
        styled=True,
    )

    mock_secho.assert_called_once_with(
        "ERROR: Version conflict",
        fg="red",
        bold=True,
        err=True,
    )

    mock_echo.assert_not_called()
