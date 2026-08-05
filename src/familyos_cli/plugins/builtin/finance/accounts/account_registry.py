"""Finance account registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.accounts.account import (
    Account,
)


class AccountRegistry:
    """Store finance accounts."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._accounts: list[Account] = []

    def add(
        self,
        account: Account,
    ) -> None:
        """Add an account."""

        self._accounts.append(
            account,
        )

    def list(
        self,
    ) -> list[Account]:
        """Return all accounts."""

        return list(
            self._accounts,
        )

    def get(
        self,
        account_id: str,
    ) -> Account | None:
        """Return account by identifier."""

        return next(
            (
                account
                for account in self._accounts
                if account.id == account_id
            ),
            None,
        )
