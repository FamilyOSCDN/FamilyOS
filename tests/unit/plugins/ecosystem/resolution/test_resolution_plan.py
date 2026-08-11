"""Tests for plugin resolution plan."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_plan import (
    ResolutionPlan,
)


def test_resolution_plan_creation() -> None:
    """A resolution plan stores packages and diagnostics."""

    package = PluginPackage(
        plugin_id="familyos.notification",
        version="1.0.0",
        source="official",
    )

    diagnostic = ResolutionDiagnostic(
        plugin="familyos.calendar",
        message="Missing dependency.",
    )

    plan = ResolutionPlan(
        ordered_packages=[package],
        skipped_packages=[],
        diagnostics=[diagnostic],
    )

    assert plan.ordered_packages == [package]
    assert plan.skipped_packages == []
    assert plan.diagnostics == [diagnostic]
