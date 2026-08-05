"""Finance account entity."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.finance.accounts.account_status import (
    AccountStatus,
)
from familyos_cli.plugins.builtin.finance.accounts.account_type import (
    AccountType,
)


@dataclass(frozen=True, slots=True)
class Account:
    """Represents a financial account."""

    id: str
    owner_id: str
    name: str
    type: AccountType
    currency: str
    status: AccountStatus = AccountStatus.ACTIVE

    def __post_init__(
        self,
    ) -> None:
        """Validate account invariants."""

        if not self.id:
            raise ValueError(
                "Account id cannot be empty.",
            )

        if not self.owner_id:
            raise ValueError(
                "Account owner id cannot be empty.",
            )

        if not self.name:
            raise ValueError(
                "Account name cannot be empty.",
            )

        if not self.currency:
            raise ValueError(
                "Account currency cannot be empty.",
            )
