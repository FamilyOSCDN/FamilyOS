"""Tests for the explanation rule protocol."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ExplanationRule,
    PluginResolutionDiagnostic,
    ResolutionExplanation,
)


class FakeExplanationRule:
    """Simple explanation rule implementation."""

    def supports(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> bool:
        return True

    def explain(
        self,
        diagnostic: PluginResolutionDiagnostic,
    ) -> ResolutionExplanation:
        return ResolutionExplanation(
            title="Test",
            summary="Test explanation.",
        )


def test_explanation_rule_protocol() -> None:
    """A concrete implementation satisfies the protocol."""

    rule: ExplanationRule = FakeExplanationRule()

    assert rule.supports(
        object(),  # type: ignore[arg-type]
    )

    explanation = rule.explain(
        object(),  # type: ignore[arg-type]
    )

    assert explanation.title == "Test"
