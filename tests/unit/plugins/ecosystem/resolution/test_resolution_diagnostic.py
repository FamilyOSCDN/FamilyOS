"""Tests for plugin resolution diagnostics."""

import pytest

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)


def test_resolution_diagnostic_creation() -> None:
    """A diagnostic should store all resolution information."""

    diagnostic = ResolutionDiagnostic(
        plugin="familyos.example",
        message="Missing dependency.",
        code=ResolutionDiagnosticCode.MISSING_DEPENDENCY,
        severity=ResolutionDiagnosticSeverity.ERROR,
    )

    assert diagnostic.plugin == "familyos.example"
    assert diagnostic.message == "Missing dependency."
    assert diagnostic.code is ResolutionDiagnosticCode.MISSING_DEPENDENCY
    assert diagnostic.severity is ResolutionDiagnosticSeverity.ERROR
    assert diagnostic.is_error is True


def test_resolution_diagnostic_preserves_existing_constructor() -> None:
    """The existing plugin-and-message constructor should remain valid."""

    diagnostic = ResolutionDiagnostic(
        plugin="familyos.example",
        message="Resolution failed.",
    )

    assert diagnostic.plugin == "familyos.example"
    assert diagnostic.message == "Resolution failed."
    assert diagnostic.code is ResolutionDiagnosticCode.UNSPECIFIED
    assert diagnostic.severity is ResolutionDiagnosticSeverity.ERROR
    assert diagnostic.is_error is True


def test_resolution_diagnostic_rejects_non_canonical_plugin_id() -> None:
    """A diagnostic should reject non-canonical plugin identifiers."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        ResolutionDiagnostic(
            plugin="example",
            message="Resolution failed.",
        )


def test_warning_diagnostic_is_not_an_error() -> None:
    """A warning diagnostic should not be classified as an error."""

    diagnostic = ResolutionDiagnostic(
        plugin="familyos.example",
        message="An optional dependency is unavailable.",
        code=ResolutionDiagnosticCode.WARNING,
        severity=ResolutionDiagnosticSeverity.WARNING,
    )

    assert diagnostic.is_error is False


def test_information_diagnostic_is_not_an_error() -> None:
    """An informational diagnostic should not be classified as an error."""

    diagnostic = ResolutionDiagnostic(
        plugin="familyos.example",
        message="Plugin resolution completed.",
        code=ResolutionDiagnosticCode.INFO,
        severity=ResolutionDiagnosticSeverity.INFO,
    )

    assert diagnostic.is_error is False
