"""Tests for the plugin resolution diagnostic model."""

import pytest

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
        plugin="familyos.crypto",
        details=(
            "familyos.security requires familyos.crypto>=3.0",
            "familyos.backup requires familyos.crypto<3.0",
        ),
        path=(
            "familyos.application",
            "familyos.security",
            "familyos.crypto",
        ),
    )

    assert diagnostic.kind is DiagnosticKind.VERSION_CONFLICT
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.message == "No compatible version exists."
    assert diagnostic.plugin == "familyos.crypto"
    assert diagnostic.details == (
        "familyos.security requires familyos.crypto>=3.0",
        "familyos.backup requires familyos.crypto<3.0",
    )
    assert diagnostic.path == (
        "familyos.application",
        "familyos.security",
        "familyos.crypto",
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


def test_plugin_resolution_diagnostic_rejects_non_canonical_plugin_id() -> None:
    """A diagnostic should reject non-canonical plugin identifiers."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginResolutionDiagnostic(
            kind=DiagnosticKind.UNKNOWN_PLUGIN,
            severity=DiagnosticSeverity.ERROR,
            message="Plugin is not available.",
            plugin="security",
        )


def test_plugin_resolution_diagnostic_rejects_non_canonical_path_id() -> None:
    """Diagnostic paths should use canonical plugin identifiers."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginResolutionDiagnostic(
            kind=DiagnosticKind.DEPENDENCY_CYCLE,
            severity=DiagnosticSeverity.ERROR,
            message="Dependency cycle detected.",
            path=(
                "familyos.security",
                "crypto",
            ),
        )


def test_plugin_resolution_diagnostic_concerns_plugin() -> None:
    """A diagnostic identifies the plugin it concerns."""

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.UNKNOWN_PLUGIN,
        severity=DiagnosticSeverity.ERROR,
        message="Plugin is not available.",
        plugin="familyos.security",
    )

    assert diagnostic.concerns("familyos.security")
    assert not diagnostic.concerns("familyos.backup")


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
