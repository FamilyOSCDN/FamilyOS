"""Finance liability entity."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from familyos_cli.plugins.builtin.finance.liabilities.liability_type import (
    LiabilityType,
)


@dataclass(frozen=True, slots=True)
class Liability:
    """Represents a family financial liability."""

    id: str
    owner_id: str
    name: str
    type: LiabilityType
    amount: Decimal
    currency: str

    def __post_init__(
        self,
    ) -> None:
        """Validate liability invariants."""

        if not self.id:
            raise ValueError(
                "Liability id cannot be empty.",
            )

        if not self.owner_id:
            raise ValueError(
                "Liability owner id cannot be empty.",
            )

        if not self.name:
            raise ValueError(
                "Liability name cannot be empty.",
            )

        if self.amount <= Decimal("0"):
            raise ValueError(
                "Liability amount must be positive.",
            )

        if not self.currency:
            raise ValueError(
                "Liability currency cannot be empty.",
            )
