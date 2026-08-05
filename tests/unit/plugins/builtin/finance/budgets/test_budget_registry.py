from decimal import Decimal

from familyos_cli.plugins.builtin.finance.budgets.budget import (
    Budget,
)
from familyos_cli.plugins.builtin.finance.budgets.budget_category import (
    BudgetCategory,
)
from familyos_cli.plugins.builtin.finance.budgets.budget_registry import (
    BudgetRegistry,
)


def create_budget(
    budget_id: str = "budget-001",
) -> Budget:
    return Budget(
        id=budget_id,
        owner_id="family-001",
        name="Food Budget",
        category=BudgetCategory.FOOD,
        limit_amount=Decimal("1000"),
        currency="EUR",
        period="monthly",
    )


def test_budget_registry_adds_budgets() -> None:
    registry = BudgetRegistry()

    registry.add(
        create_budget(),
    )

    assert len(
        registry.list(),
    ) == 1


def test_budget_registry_gets_budget_by_id() -> None:
    registry = BudgetRegistry()

    registry.add(
        create_budget(),
    )

    budget = registry.get(
        "budget-001",
    )

    assert budget is not None
    assert budget.id == "budget-001"


def test_budget_registry_returns_none_for_unknown_id() -> None:
    registry = BudgetRegistry()

    assert registry.get(
        "unknown",
    ) is None
