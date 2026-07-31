"""Plugin resolution diagnostic model."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_kind import (
    DiagnosticKind,
)
from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_severity import (
    DiagnosticSeverity,
)


@dataclass(frozen=True, slots=True)
class PluginResolutionDiagnostic:
    """Describe an issue or information produced during plugin resolution."""

    kind: DiagnosticKind
    severity: DiagnosticSeverity
    message: str
    plugin: str = ""
    details: tuple[str, ...] = field(default_factory=tuple)
    path: tuple[str, ...] = field(default_factory=tuple)

    def concerns(self, plugin_name: str) -> bool:
        """Return whether this diagnostic concerns the given plugin."""

        return self.plugin == plugin_name

    def is_error(self) -> bool:
        """Return whether the diagnostic represents an error."""

        return self.severity is DiagnosticSeverity.ERROR

    def is_warning(self) -> bool:
        """Return whether the diagnostic represents a warning."""

        return self.severity is DiagnosticSeverity.WARNING

    def is_info(self) -> bool:
        """Return whether the diagnostic represents information."""

        return self.severity is DiagnosticSeverity.INFO
