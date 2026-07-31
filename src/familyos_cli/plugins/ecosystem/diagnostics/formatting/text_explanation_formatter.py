"""Text explanation formatter."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)


class TextExplanationFormatter:
    """Format explanations as human-readable text."""

    def format(
        self,
        explanation: ResolutionExplanation,
    ) -> str:
        """Format an explanation."""

        sections: list[str] = [
            explanation.title,
            "",
            explanation.summary,
        ]

        if explanation.causes:
            sections.extend(
                [
                    "",
                    "Causes:",
                    *(
                        f"- {cause}"
                        for cause in explanation.causes
                    ),
                ]
            )

        if explanation.suggestions:
            sections.extend(
                [
                    "",
                    "Suggestions:",
                    *(
                        f"- {suggestion}"
                        for suggestion in explanation.suggestions
                    ),
                ]
            )

        return "\n".join(
            sections,
        )
