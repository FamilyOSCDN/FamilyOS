"""JSON explanation formatter."""

from __future__ import annotations

import json

from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)


class JsonExplanationFormatter:
    """Format explanations as JSON."""

    def format(
        self,
        explanation: ResolutionExplanation,
    ) -> str:
        """Format an explanation as JSON."""

        return json.dumps(
            {
                "title": explanation.title,
                "summary": explanation.summary,
                "causes": list(
                    explanation.causes,
                ),
                "suggestions": list(
                    explanation.suggestions,
                ),
            },
            indent=2,
        )
