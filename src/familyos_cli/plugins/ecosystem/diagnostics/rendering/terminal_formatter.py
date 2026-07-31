"""Terminal formatter for diagnostic explanations."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.explaining import (
    ResolutionExplanation,
)


class TerminalFormatter:
    """Format diagnostic explanations for terminal output."""

    def format(
        self,
        explanation: ResolutionExplanation,
    ) -> str:
        """Return a terminal-friendly representation."""

        lines: list[str] = [
            f"ERROR: {explanation.title}",
            "",
            explanation.summary,
        ]

        if explanation.causes:
            lines.extend(
                [
                    "",
                    "Causes:",
                    *(f"- {cause}" for cause in explanation.causes),
                ],
            )

        if explanation.suggestions:
            lines.extend(
                [
                    "",
                    "Suggestions:",
                    *(f"- {suggestion}" for suggestion in explanation.suggestions),
                ],
            )

        return "\n".join(lines)
