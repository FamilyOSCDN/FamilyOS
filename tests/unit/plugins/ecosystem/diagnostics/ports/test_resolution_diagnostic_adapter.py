"""Tests for the resolution diagnostic adapter protocol."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    PluginResolutionDiagnostic,
    ResolutionDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.resolution import ResolutionPlan


class FakeResolutionDiagnosticAdapter:
    """Simple protocol implementation."""

    def adapt(
        self,
        plan: ResolutionPlan,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        return ()


def test_resolution_diagnostic_adapter_protocol() -> None:
    """A concrete adapter satisfies the protocol."""

    adapter: ResolutionDiagnosticAdapter = (
        FakeResolutionDiagnosticAdapter()
    )

    assert adapter.adapt(ResolutionPlan()) == ()
