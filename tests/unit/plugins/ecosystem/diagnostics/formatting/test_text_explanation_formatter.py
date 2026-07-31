"""Tests for the text explanation formatter."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ResolutionExplanation,
    TextExplanationFormatter,
)


def test_formats_complete_explanation() -> None:
    """A complete explanation is rendered."""

    explanation = ResolutionExplanation(
        title="Dependency cycle detected",
        summary=(
            "Plugins cannot be resolved "
            "because they depend on each other."
        ),
        causes=(
            "security depends on crypto",
        ),
        suggestions=(
            "Remove one dependency.",
        ),
    )

    result = TextExplanationFormatter().format(
        explanation,
    )

    assert result == (
        "Dependency cycle detected\n\n"
        "Plugins cannot be resolved "
        "because they depend on each other.\n\n"
        "Causes:\n"
        "- security depends on crypto\n\n"
        "Suggestions:\n"
        "- Remove one dependency."
    )


def test_formats_explanation_without_optional_sections() -> None:
    """An explanation without details stays readable."""

    explanation = ResolutionExplanation(
        title="Resolution issue",
        summary="An issue occurred.",
    )

    result = TextExplanationFormatter().format(
        explanation,
    )

    assert result == (
        "Resolution issue\n\n"
        "An issue occurred."
    )
