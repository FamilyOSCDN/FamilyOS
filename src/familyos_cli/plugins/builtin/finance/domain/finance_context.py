"""Finance context model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.finance.domain.finance_level import (
    FinanceLevel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class FinanceContext:
    """Context used for finance evaluation."""

    domain_name: str

    subject: str

    required_level: FinanceLevel
