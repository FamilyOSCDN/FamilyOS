"""Tests for plugin resolution diagnostic kinds."""

from familyos_cli.plugins.ecosystem.diagnostics import DiagnosticKind


def test_diagnostic_kind_values() -> None:
    """Diagnostic kinds expose stable serialized values."""

    assert DiagnosticKind.VERSION_CONFLICT.value == "version_conflict"
    assert DiagnosticKind.DEPENDENCY_CYCLE.value == "dependency_cycle"
    assert DiagnosticKind.MISSING_DEPENDENCY.value == "missing_dependency"
    assert DiagnosticKind.UNKNOWN_PLUGIN.value == "unknown_plugin"
    assert DiagnosticKind.INVALID_PACKAGE.value == "invalid_package"
    assert DiagnosticKind.RESOLUTION_FAILURE.value == "resolution_failure"
    assert DiagnosticKind.INFORMATION.value == "information"
