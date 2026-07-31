"""Tests for plugin resolution diagnostic kinds."""

from familyos_cli.plugins.ecosystem.diagnostics import DiagnosticKind


def test_diagnostic_kind_values() -> None:
    """Diagnostic kinds expose stable serialized values."""

    assert DiagnosticKind.VERSION_CONFLICT == "version_conflict"
    assert DiagnosticKind.DEPENDENCY_CYCLE == "dependency_cycle"
    assert DiagnosticKind.MISSING_DEPENDENCY == "missing_dependency"
    assert DiagnosticKind.UNKNOWN_PLUGIN == "unknown_plugin"
    assert DiagnosticKind.INVALID_PACKAGE == "invalid_package"
    assert DiagnosticKind.RESOLUTION_FAILURE == "resolution_failure"
    assert DiagnosticKind.INFORMATION == "information"
