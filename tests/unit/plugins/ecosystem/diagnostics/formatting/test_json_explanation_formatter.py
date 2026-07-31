"""Tests for the JSON explanation formatter."""

import json

from familyos_cli.plugins.ecosystem.diagnostics import (
    JsonExplanationFormatter,
    ResolutionExplanation,
)


def test_formats_explanation_as_json() -> None:
    """A resolution explanation is serialized."""

    explanation = ResolutionExplanation(
        title="Dependency cycle detected",
        summary=(
            "Plugins cannot be resolved."
        ),
        causes=(
            "security depends on crypto",
        ),
        suggestions=(
            "Remove one dependency.",
        ),
    )

    result = JsonExplanationFormatter().format(
        explanation,
    )

    payload = json.loads(
        result,
    )

    assert payload == {
        "title": "Dependency cycle detected",
        "summary": (
            "Plugins cannot be resolved."
        ),
        "causes": [
            "security depends on crypto",
        ],
        "suggestions": [
            "Remove one dependency.",
        ],
    }


def test_formats_empty_collections() -> None:
    """Empty sections remain JSON arrays."""

    result = JsonExplanationFormatter().format(
        ResolutionExplanation(
            title="Issue",
            summary="Problem.",
        ),
    )

    payload = json.loads(
        result,
    )

    assert payload["causes"] == []
    assert payload["suggestions"] == []
