"""Tests for the plugin resolution diagnostic model."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
)


def test_plugin_resolution_diagnostic_creation() -> None:
    """A diagnostic stores its resolution context."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.VERSION_CONFLICT,
        severity=DiagnosticSeverity.ERROR,
        message="No compatible version exists.",
        plugin="crypto",
        details=(
            "security requires crypto>=3.0",
            "backup requires crypto<3.0",
        ),
        path=("application", "security", "crypto"),
    )

    assert diagnostic.kind is DiagnosticKind.VERSION_CONFLICT
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.message == "No compatible version exists."
    assert diagnostic.plugin == "crypto"
    assert diagnostic.details == (
        "security requires crypto>=3.0",
        "backup requires crypto<3.0",
    )
    assert diagnostic.path == (
        "application",
        "security",
        "crypto",
    )


def test_plugin_resolution_diagnostic_defaults() -> None:
    """Optional diagnostic context defaults to immutable empty tuples."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.INFORMATION,
        severity=DiagnosticSeverity.INFO,
        message="Resolution completed.",
    )

    assert diagnostic.plugin == ""
    assert diagnostic.details == ()
    assert diagnostic.path == ()


def test_plugin_resolution_diagnostic_concerns_plugin() -> None:
    """A diagnostic identifies the plugin it concerns."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.UNKNOWN_PLUGIN,
        severity=DiagnosticSeverity.ERROR,
        message="Plugin is not available.",
        plugin="security",
    )

    assert diagnostic.concerns("security")
    assert not diagnostic.concerns("backup")


def test_plugin_resolution_diagnostic_severity_helpers() -> None:
    """Severity helpers reflect the diagnostic severity."""

    error = PluginResolutionDiagnostic(
        kind=DiagnosticKind.RESOLUTION_FAILURE,
        severity=DiagnosticSeverity.ERROR,
        message="Resolution failed.",
    )
    warning = PluginResolutionDiagnostic(
        kind=DiagnosticKind.INVALID_PACKAGE,
        severity=DiagnosticSeverity.WARNING,
        message="Package metadata is incomplete.",
    )
    info = PluginResolutionDiagnostic(
        kind=DiagnosticKind.INFORMATION,
        severity=DiagnosticSeverity.INFO,
        message="Resolution started.",
    )

    assert error.is_error()
    assert not error.is_warning()
    assert not error.is_info()

    assert warning.is_warning()
    assert not warning.is_error()
    assert not warning.is_info()

    assert info.is_info()
    assert not info.is_error()
    assert not info.is_warning()
