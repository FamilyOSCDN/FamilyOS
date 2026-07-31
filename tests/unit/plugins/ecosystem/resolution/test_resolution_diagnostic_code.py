"""Tests for plugin resolution diagnostic codes."""

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)


def test_resolution_diagnostic_codes_have_stable_values() -> None:
    """Diagnostic codes should expose stable serialized values."""

    assert ResolutionDiagnosticCode.UNSPECIFIED == "unspecified"
    assert ResolutionDiagnosticCode.CYCLE_DETECTED == "cycle_detected"
    assert ResolutionDiagnosticCode.MISSING_PLUGIN == "missing_plugin"
    assert ResolutionDiagnosticCode.MISSING_DEPENDENCY == "missing_dependency"
    assert ResolutionDiagnosticCode.VERSION_CONFLICT == "version_conflict"
    assert (
        ResolutionDiagnosticCode.UNSATISFIABLE_CONSTRAINT
        == "unsatisfiable_constraint"
    )
    assert ResolutionDiagnosticCode.WARNING == "warning"
    assert ResolutionDiagnosticCode.INFO == "info"
