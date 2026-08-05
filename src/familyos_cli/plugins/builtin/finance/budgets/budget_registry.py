"""Finance budget registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.finance.budgets.budget import (
    Budget,
)


class BudgetRegistry:
    """Store financial budgets."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._budgets: list[Budget] = []

    def add(
        self,
        budget: Budget,
    ) -> None:
        """Add a budget."""

        self._budgets.append(
            budget,
        )

    def list(
        self,
    ) -> list[Budget]:
        """Return all budgets."""

        return list(
            self._budgets,
        )

    def get(
        self,
        budget_id: str,
    ) -> Budget | None:
        """Return budget by identifier."""

        return next(
            (
                budget
                for budget in self._budgets
                if budget.id == budget_id
            ),
            None,
        )
