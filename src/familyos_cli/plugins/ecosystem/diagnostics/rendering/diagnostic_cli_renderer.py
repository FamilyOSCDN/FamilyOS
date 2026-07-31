"""CLI diagnostic renderer."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.explaining import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.rendering.terminal_formatter import (
    TerminalFormatter,
)


class DiagnosticCliRenderer:
    """Render diagnostic explanations for CLI output."""

    def __init__(
        self,
        formatter: TerminalFormatter | None = None,
    ) -> None:
        """Initialize the renderer."""

        self._formatter = formatter or TerminalFormatter()

    def render(
        self,
        explanation: ResolutionExplanation,
    ) -> str:
        """Render an explanation for CLI output."""

        return self._formatter.format(explanation)
