"""Tests for resolution suggestions."""

from familyos_cli.plugins.ecosystem.diagnostics.suggestions import (
    ResolutionSuggestion,
)


def test_resolution_suggestion_creation() -> None:
    """A suggestion stores its message."""

    suggestion = ResolutionSuggestion(
        message="Install the missing plugin.",
    )

    assert suggestion.message == "Install the missing plugin."


def test_empty_suggestion() -> None:
    """Whitespace-only suggestions are considered empty."""

    suggestion = ResolutionSuggestion(
        message="   ",
    )

    assert suggestion.is_empty()


def test_non_empty_suggestion() -> None:
    """A populated suggestion is not empty."""

    suggestion = ResolutionSuggestion(
        message="Enable the repository.",
    )

    assert not suggestion.is_empty()
