"""Tests for diagnostic CLI output."""

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
