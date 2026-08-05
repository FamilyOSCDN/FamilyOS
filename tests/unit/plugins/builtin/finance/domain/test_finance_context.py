"""Tests for FinanceContext."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)


def test_finance_context_can_be_created() -> None:
    """Finance context stores values."""

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.STANDARD,
    )

    assert context.domain_name == "family"
    assert context.subject == "member"
    assert context.required_level == FinanceLevel.STANDARD


def test_finance_context_is_immutable() -> None:
    """Finance context cannot be modified."""

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.BASIC,
    )

    with pytest.raises(FrozenInstanceError):
        context.subject = "other"  # type: ignore[misc]
