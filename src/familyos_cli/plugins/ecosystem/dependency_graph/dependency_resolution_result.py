"""Plugin dependency graph resolution result."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.dependency_graph.plugin_node import (
    PluginNode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic import (
    ResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DependencyResolutionResult:
    """Represent the result of resolving a plugin dependency graph."""

    ordered_nodes: tuple[PluginNode, ...]
    cycle_detected: bool
    diagnostics: tuple[ResolutionDiagnostic, ...] = ()

    @property
    def succeeded(
        self,
    ) -> bool:
        """Return whether dependency graph resolution succeeded."""

        return not any(
            diagnostic.is_error
            for diagnostic in self.diagnostics
        )

    @classmethod
    def resolved(
        cls,
        ordered_nodes: tuple[PluginNode, ...],
        diagnostics: tuple[ResolutionDiagnostic, ...] = (),
    ) -> DependencyResolutionResult:
        """Create a successful dependency resolution result."""

        return cls(
            ordered_nodes=ordered_nodes,
            cycle_detected=False,
            diagnostics=diagnostics,
        )

    @classmethod
    def cyclic(
        cls,
    ) -> DependencyResolutionResult:
        """Create a result representing a dependency cycle."""

        diagnostic = ResolutionDiagnostic(
            plugin="",
            message="Dependency cycle detected.",
            code=ResolutionDiagnosticCode.CYCLE_DETECTED,
            severity=ResolutionDiagnosticSeverity.ERROR,
        )

        return cls(
            ordered_nodes=(),
            cycle_detected=True,
            diagnostics=(
                diagnostic,
            ),
        )
