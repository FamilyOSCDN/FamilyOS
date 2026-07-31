"""Plugin resolution diagnostic model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ResolutionDiagnostic:
    """Describe a diagnostic produced during plugin resolution."""

    plugin: str
    message: str
    code: ResolutionDiagnosticCode = ResolutionDiagnosticCode.UNSPECIFIED
    severity: ResolutionDiagnosticSeverity = ResolutionDiagnosticSeverity.ERROR

    @property
    def is_error(
        self,
    ) -> bool:
        """Return whether the diagnostic represents an error."""

        return self.severity is ResolutionDiagnosticSeverity.ERROR
