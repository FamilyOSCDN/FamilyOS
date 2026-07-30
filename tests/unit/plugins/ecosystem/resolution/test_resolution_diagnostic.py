"""Tests for plugin resolution diagnostics."""

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)


def test_resolution_diagnostic_creation() -> None:
    """A diagnostic should store its plugin and message."""

    diagnostic = ResolutionDiagnostic(
        plugin="example",
        message="Missing dependency.",
    )

    assert diagnostic.plugin == "example"
    assert diagnostic.message == "Missing dependency."
