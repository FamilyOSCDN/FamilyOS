from decimal import Decimal

from pytest import raises

from familyos_cli.plugins.builtin.finance.budgets.budget import (
    Budget,
)
from familyos_cli.plugins.builtin.finance.budgets.budget_category import (
    BudgetCategory,
)


def create_budget(
    limit_amount: Decimal = Decimal("1000"),
    budget_id: str = "budget-001",
) -> Budget:
    return Budget(
        id=budget_id,
        owner_id="family-001",
        name="Monthly Food Budget",
        category=BudgetCategory.FOOD,
        limit_amount=limit_amount,
        currency="EUR",
        period="monthly",
    )


def test_budget_can_be_created() -> None:
    budget = create_budget()

    assert budget.id == "budget-001"
    assert budget.owner_id == "family-001"
    assert budget.name == "Monthly Food Budget"
    assert budget.category == BudgetCategory.FOOD
    assert budget.limit_amount == Decimal("1000")
    assert budget.currency == "EUR"
    assert budget.period == "monthly"


def test_budget_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Budget id cannot be empty.",
    ):
        create_budget(
            budget_id="",
        )


def test_budget_rejects_empty_owner_id() -> None:
    with raises(
        ValueError,
        match="Budget owner id cannot be empty.",
    ):
        Budget(
            id="budget-001",
            owner_id="",
            name="Food",
            category=BudgetCategory.FOOD,
            limit_amount=Decimal("1000"),
            currency="EUR",
            period="monthly",
        )


def test_budget_rejects_empty_name() -> None:
    with raises(
        ValueError,
        match="Budget name cannot be empty.",
    ):
        Budget(
            id="budget-001",
            owner_id="family-001",
            name="",
            category=BudgetCategory.FOOD,
            limit_amount=Decimal("1000"),
            currency="EUR",
            period="monthly",
        )


def test_budget_rejects_non_positive_limit_amount() -> None:
    with raises(
        ValueError,
        match="Budget limit amount must be positive.",
    ):
        create_budget(
            limit_amount=Decimal("0"),
        )


def test_budget_rejects_empty_currency() -> None:
    with raises(
        ValueError,
        match="Budget currency cannot be empty.",
    ):
        Budget(
            id="budget-001",
            owner_id="family-001",
            name="Food",
            category=BudgetCategory.FOOD,
            limit_amount=Decimal("1000"),
            currency="",
            period="monthly",
        )


def test_budget_rejects_empty_period() -> None:
    with raises(
        ValueError,
        match="Budget period cannot be empty.",
    ):
        Budget(
            id="budget-001",
            owner_id="family-001",
            name="Food",
            category=BudgetCategory.FOOD,
            limit_amount=Decimal("1000"),
            currency="EUR",
            period="",
        )
