"""Tests for FinanceRule."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.finance.rules.finance_rule import (
    FinanceRule,
)


def test_finance_rule_can_be_created() -> None:
    """Finance rule stores values."""

    rule = FinanceRule(
        id="finance.rule.transaction-limit",
        name="Transaction Limit Rule",
        version="1.0.0",
        severity="HIGH",
        description="Checks transaction limits.",
    )

    assert rule.id == "finance.rule.transaction-limit"
    assert rule.name == "Transaction Limit Rule"
    assert rule.version == "1.0.0"
    assert rule.severity == "HIGH"
    assert rule.description == (
        "Checks transaction limits."
    )


def test_finance_rule_description_is_optional() -> None:
    """Description defaults to empty."""

    rule = FinanceRule(
        id="finance.rule.basic",
        name="Basic Finance Rule",
        version="1.0.0",
        severity="LOW",
    )

    assert rule.description == ""


def test_finance_rule_is_immutable() -> None:
    """Finance rules cannot be modified."""

    rule = FinanceRule(
        id="finance.rule.basic",
        name="Basic Finance Rule",
        version="1.0.0",
        severity="LOW",
    )

    with pytest.raises(FrozenInstanceError):
        rule.severity = "HIGH"  # type: ignore[misc]
