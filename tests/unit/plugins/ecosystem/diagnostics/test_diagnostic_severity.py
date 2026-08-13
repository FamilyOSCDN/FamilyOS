"""Tests for plugin resolution diagnostic severity levels."""

from familyos_cli.plugins.ecosystem.diagnostics import DiagnosticSeverity


def test_diagnostic_severity_values() -> None:
    """Diagnostic severities expose stable serialized values."""

    assert DiagnosticSeverity.INFO.value == "info"
    assert DiagnosticSeverity.WARNING.value == "warning"
    assert DiagnosticSeverity.ERROR.value == "error"
