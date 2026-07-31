"""Plugin resolution diagnostic report builder."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_report import (
    DiagnosticReport,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


@dataclass(slots=True)
class DiagnosticBuilder:
    """Build a plugin resolution diagnostic report incrementally."""

    _diagnostics: list[PluginResolutionDiagnostic] = field(
        default_factory=list,
    )

    def add(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> DiagnosticBuilder:
        """Add a diagnostic and return this builder."""

        self._diagnostics.append(diagnostic)
        return self

    def add_many(
        self,
        diagnostics: tuple[PluginResolutionDiagnostic, ...],
    ) -> DiagnosticBuilder:
        """Add multiple diagnostics and return this builder."""

        self._diagnostics.extend(diagnostics)
        return self

    def build(self) -> DiagnosticReport:
        """Build an immutable diagnostic report."""

        return DiagnosticReport(
            diagnostics=tuple(self._diagnostics),
        )

    def clear(self) -> DiagnosticBuilder:
        """Remove all accumulated diagnostics and return this builder."""

        self._diagnostics.clear()
        return self

    def is_empty(self) -> bool:
        """Return whether the builder contains no diagnostics."""

        return not self._diagnostics

    def count(self) -> int:
        """Return the number of accumulated diagnostics."""

        return len(self._diagnostics)
