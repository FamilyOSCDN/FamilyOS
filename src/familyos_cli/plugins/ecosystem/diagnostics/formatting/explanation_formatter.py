"""Explanation formatter protocol."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.plugins.ecosystem.diagnostics.explaining.resolution_explanation import (
    ResolutionExplanation,
)


class ExplanationFormatter(Protocol):
    """Define a formatter for resolution explanations."""

    def format(
        self,
        explanation: ResolutionExplanation,
    ) -> str:
        """Format an explanation into an external representation."""
