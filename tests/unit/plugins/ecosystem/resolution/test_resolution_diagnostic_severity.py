"""Tests for plugin resolution diagnostic severities."""

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)


def test_resolution_diagnostic_severities_have_stable_values() -> None:
    """Diagnostic severities should expose stable serialized values."""

    assert ResolutionDiagnosticSeverity.INFO.value == "info"
    assert ResolutionDiagnosticSeverity.WARNING.value == "warning"
    assert ResolutionDiagnosticSeverity.ERROR.value == "error"
