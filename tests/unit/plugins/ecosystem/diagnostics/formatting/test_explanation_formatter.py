"""Tests for the explanation formatter protocol."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ExplanationFormatter,
    ResolutionExplanation,
)


class FakeFormatter:
    """Simple formatter implementation."""

    def format(
        self,
        explanation: ResolutionExplanation,
    ) -> str:
        return explanation.title


def test_explanation_formatter_protocol() -> None:
    """A formatter implementation satisfies the protocol."""

    formatter: ExplanationFormatter = FakeFormatter()

    result = formatter.format(
        ResolutionExplanation(
            title="Test",
            summary="Test explanation.",
        ),
    )

    assert result == "Test"
