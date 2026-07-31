"""Tests for the resolution explanation model."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ResolutionExplanation,
)


def test_resolution_explanation_creation() -> None:
    """An explanation stores all human-facing information."""

    explanation = ResolutionExplanation(
        title="Dependency cycle detected",
        summary=(
            "Plugins cannot be resolved because "
            "they depend on each other."
        ),
        causes=(
            "security depends on crypto",
            "crypto depends on security",
        ),
        suggestions=(
            "Remove one dependency.",
        ),
    )

    assert explanation.title == (
        "Dependency cycle detected"
    )
    assert explanation.summary == (
        "Plugins cannot be resolved because "
        "they depend on each other."
    )
    assert explanation.causes == (
        "security depends on crypto",
        "crypto depends on security",
    )
    assert explanation.suggestions == (
        "Remove one dependency.",
    )


def test_resolution_explanation_defaults_to_empty_collections() -> None:
    """Causes and suggestions are optional."""

    explanation = ResolutionExplanation(
        title="Missing dependency",
        summary="A required plugin is unavailable.",
    )

    assert explanation.causes == ()
    assert explanation.suggestions == ()


def test_resolution_explanation_detects_causes() -> None:
    """The model reports whether causes exist."""

    with_causes = ResolutionExplanation(
        title="Conflict",
        summary="Version conflict.",
        causes=("A requires B.",),
    )

    without_causes = ResolutionExplanation(
        title="Conflict",
        summary="Version conflict.",
    )

    assert with_causes.has_causes()
    assert not without_causes.has_causes()


def test_resolution_explanation_detects_suggestions() -> None:
    """The model reports whether suggestions exist."""

    with_suggestions = ResolutionExplanation(
        title="Conflict",
        summary="Version conflict.",
        suggestions=("Update plugin.",),
    )

    without_suggestions = ResolutionExplanation(
        title="Conflict",
        summary="Version conflict.",
    )

    assert with_suggestions.has_suggestions()
    assert not without_suggestions.has_suggestions()
