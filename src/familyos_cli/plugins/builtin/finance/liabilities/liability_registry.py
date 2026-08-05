"""Finance liability registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.liabilities.liability import (
    Liability,
)


class LiabilityRegistry:
    """Store financial liabilities."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._liabilities: list[Liability] = []

    def add(
        self,
        liability: Liability,
    ) -> None:
        """Add a liability."""

        self._liabilities.append(
            liability,
        )

    def list(
        self,
    ) -> list[Liability]:
        """Return all liabilities."""

        return list(
            self._liabilities,
        )

    def get(
        self,
        liability_id: str,
    ) -> Liability | None:
        """Return liability by identifier."""

        return next(
            (
                liability
                for liability in self._liabilities
                if liability.id == liability_id
            ),
            None,
        )
