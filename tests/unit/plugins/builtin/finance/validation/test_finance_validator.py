"""Tests for FinanceValidator."""

from familyos_cli.plugins.builtin.finance.domain.finance_context import (
    FinanceContext,
)
from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)
from familyos_cli.plugins.builtin.finance.validation.finance_validator import (
    FinanceValidator,
)


def test_standard_context_is_valid() -> None:
    """Standard finance context should be valid."""

    validator = FinanceValidator()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.STANDARD,
    )

    result = validator.validate(
        context,
    )

    assert result.valid is True
    assert result.message == (
        "Finance context validated."
    )


def test_critical_context_requires_review() -> None:
    """Critical finance context should fail validation."""

    validator = FinanceValidator()

    context = FinanceContext(
        domain_name="family",
        subject="member",
        required_level=FinanceLevel.CRITICAL,
    )

    result = validator.validate(
        context,
    )

    assert result.valid is False
    assert result.message == (
        "Critical finance review required."
    )
