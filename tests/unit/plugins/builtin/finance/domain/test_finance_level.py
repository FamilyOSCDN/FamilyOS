"""Tests for FinanceLevel."""

from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)


def test_finance_level_values() -> None:
    """Finance levels expose expected values."""

    assert FinanceLevel.BASIC.value == "basic"
    assert FinanceLevel.STANDARD.value == "standard"
    assert FinanceLevel.SENSITIVE.value == "sensitive"
    assert FinanceLevel.CRITICAL.value == "critical"
