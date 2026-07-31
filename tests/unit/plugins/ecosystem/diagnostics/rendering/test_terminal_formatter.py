"""Tests for terminal formatter."""

from familyos_cli.plugins.ecosystem.diagnostics.explaining import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.rendering import (
    TerminalFormatter,
)


def test_formats_complete_explanation() -> None:
    """Formatter renders a complete explanation."""

    explanation = ResolutionExplanation(
        title="Missing dependency",
        summary="A dependency is missing.",
        causes=("plugin-a requires plugin-b",),
        suggestions=("Install plugin-b.",),
    )

    result = TerminalFormatter().format(explanation)

    assert result == (
        "ERROR: Missing dependency\n\n"
        "A dependency is missing.\n\n"
        "Causes:\n"
        "- plugin-a requires plugin-b\n\n"
        "Suggestions:\n"
        "- Install plugin-b."
    )
