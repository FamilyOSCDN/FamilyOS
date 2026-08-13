"""Tests for canonical compliance rule outcomes."""

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome


def test_rule_outcome_values() -> None:
    """Rule outcomes expose stable serialized values."""

    assert RuleOutcome.PASS.value == "pass"
    assert RuleOutcome.FAIL.value == "fail"
    assert RuleOutcome.NOT_APPLICABLE.value == "not_applicable"
    assert RuleOutcome.NOT_EVALUATED.value == "not_evaluated"
    assert RuleOutcome.ERROR.value == "error"
