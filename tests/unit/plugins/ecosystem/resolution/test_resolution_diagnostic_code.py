"""Tests for plugin resolution diagnostic codes."""

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)


def test_resolution_diagnostic_codes_have_stable_values() -> None:
    """Diagnostic codes should expose stable serialized values."""

    assert ResolutionDiagnosticCode.UNSPECIFIED.value == "unspecified"
    assert ResolutionDiagnosticCode.CYCLE_DETECTED.value == "cycle_detected"
    assert ResolutionDiagnosticCode.MISSING_PLUGIN.value == "missing_plugin"
    assert ResolutionDiagnosticCode.MISSING_DEPENDENCY.value == "missing_dependency"
    assert ResolutionDiagnosticCode.VERSION_CONFLICT.value == "version_conflict"
    assert (
        ResolutionDiagnosticCode.UNSATISFIABLE_CONSTRAINT.value
        == "unsatisfiable_constraint"
    )
    assert ResolutionDiagnosticCode.WARNING.value == "warning"
    assert ResolutionDiagnosticCode.INFO.value == "info"
