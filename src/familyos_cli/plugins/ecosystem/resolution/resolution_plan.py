"""Plugin resolution plan."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)


@dataclass(frozen=True, slots=True)
class ResolutionPlan:
    """Represents the result of plugin dependency resolution."""

    ordered_packages: list[PluginPackage] = field(
        default_factory=list,
    )
    skipped_packages: list[PluginPackage] = field(
        default_factory=list,
    )
    diagnostics: list[ResolutionDiagnostic] = field(
        default_factory=list,
    )
