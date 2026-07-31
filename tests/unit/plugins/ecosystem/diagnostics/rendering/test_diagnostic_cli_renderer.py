"""Tests for the CLI diagnostic renderer."""

from familyos_cli.plugins.ecosystem.diagnostics.explaining import (
    ResolutionExplanation,
)
from familyos_cli.plugins.ecosystem.diagnostics.rendering import (
    DiagnosticCliRenderer,
)


def test_renders_complete_cli_diagnostic() -> None:
    """A complete explanation is rendered for terminal output."""

    explanation = ResolutionExplanation(
        title="Missing plugin dependency",
        summary=(
            "A required plugin dependency "
            "is not available."
        ),
        causes=(
            "security requires crypto",
        ),
        suggestions=(
            "Install the missing plugin.",
        ),
    )

    result = DiagnosticCliRenderer().render(explanation)

    assert result == (
        "ERROR: Missing plugin dependency\n\n"
        "A required plugin dependency "
        "is not available.\n\n"
        "Causes:\n"
        "- security requires crypto\n\n"
        "Suggestions:\n"
        "- Install the missing plugin."
    )


def test_omits_causes_when_none_are_available() -> None:
    """The causes section is omitted when it is empty."""

    explanation = ResolutionExplanation(
        title="Resolution failed",
        summary="The plugin set could not be resolved.",
        causes=(),
        suggestions=(
            "Review the requested plugin versions.",
        ),
    )

    result = DiagnosticCliRenderer().render(explanation)

    assert result == (
        "ERROR: Resolution failed\n\n"
        "The plugin set could not be resolved.\n\n"
        "Suggestions:\n"
        "- Review the requested plugin versions."
    )


def test_omits_suggestions_when_none_are_available() -> None:
    """The suggestions section is omitted when it is empty."""

    explanation = ResolutionExplanation(
        title="Dependency cycle",
        summary="A dependency cycle was detected.",
        causes=(
            "plugin-a requires plugin-b",
            "plugin-b requires plugin-a",
        ),
        suggestions=(),
    )

    result = DiagnosticCliRenderer().render(explanation)

    assert result == (
        "ERROR: Dependency cycle\n\n"
        "A dependency cycle was detected.\n\n"
        "Causes:\n"
        "- plugin-a requires plugin-b\n"
        "- plugin-b requires plugin-a"
    )


def test_renders_summary_only() -> None:
    """An explanation may contain only a title and summary."""

    explanation = ResolutionExplanation(
        title="Resolution failed",
        summary="No compatible resolution was found.",
        causes=(),
        suggestions=(),
    )

    result = DiagnosticCliRenderer().render(explanation)

    assert result == (
        "ERROR: Resolution failed\n\n"
        "No compatible resolution was found."
    )
