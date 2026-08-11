"""Plugin resolution diagnostic model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_code import (
    ResolutionDiagnosticCode,
)
from familyos_cli.plugins.ecosystem.resolution.resolution_diagnostic_severity import (
    ResolutionDiagnosticSeverity,
)
from familyos_cli.plugins.identity import PluginId


@dataclass(
    frozen=True,
    slots=True,
)
class ResolutionDiagnostic:
    """Describe a diagnostic produced during plugin resolution."""

    message: str
    plugin: str | None = None
    code: ResolutionDiagnosticCode = ResolutionDiagnosticCode.UNSPECIFIED
    severity: ResolutionDiagnosticSeverity = ResolutionDiagnosticSeverity.ERROR

    def __post_init__(
        self,
    ) -> None:
        """Validate the plugin identifier when one is provided."""

        if self.plugin is None:
            return

        canonical_plugin_id = PluginId(
            self.plugin,
        ).value

        object.__setattr__(
            self,
            "plugin",
            canonical_plugin_id,
        )

    @property
    def is_error(
        self,
    ) -> bool:
        """Return whether the diagnostic represents an error."""

        return self.severity is ResolutionDiagnosticSeverity.ERROR
