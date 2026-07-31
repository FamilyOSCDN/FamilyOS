"""Plugin resolution diagnostic report."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)
from familyos_cli.plugins.ecosystem.diagnostics.plugin_resolution_diagnostic import (
    PluginResolutionDiagnostic,
)


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    """Aggregate diagnostics produced during plugin resolution."""

    diagnostics: tuple[PluginResolutionDiagnostic, ...] = field(
        default_factory=tuple,
    )

    def add(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> DiagnosticReport:
        """Return a new report containing the given diagnostic."""

        return DiagnosticReport(
            diagnostics=(*self.diagnostics, diagnostic),
        )

    def extend(
        self,
        diagnostics: tuple[PluginResolutionDiagnostic, ...],
    ) -> DiagnosticReport:
        """Return a new report containing the given diagnostics."""

        return DiagnosticReport(
            diagnostics=(*self.diagnostics, *diagnostics),
        )

    def errors(self) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return all error diagnostics."""

        return self._with_severity(DiagnosticSeverity.ERROR)

    def warnings(self) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return all warning diagnostics."""

        return self._with_severity(DiagnosticSeverity.WARNING)

    def infos(self) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return all informational diagnostics."""

        return self._with_severity(DiagnosticSeverity.INFO)

    def has_errors(self) -> bool:
        """Return whether the report contains at least one error."""

        return bool(self.errors())

    def is_success(self) -> bool:
        """Return whether the report contains no errors."""

        return not self.has_errors()

    def is_empty(self) -> bool:
        """Return whether the report contains no diagnostics."""

        return not self.diagnostics

    def _with_severity(
        self,
        severity: DiagnosticSeverity,
    ) -> tuple[PluginResolutionDiagnostic, ...]:
        """Return diagnostics matching the given severity."""

        return tuple(
            diagnostic
            for diagnostic in self.diagnostics
            if diagnostic.severity is severity
        )
