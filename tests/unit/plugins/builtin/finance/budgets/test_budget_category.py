from familyos_cli.plugins.builtin.finance.budgets.budget_category import (
    BudgetCategory,
)


def test_budget_category_contains_expected_values() -> None:
    assert BudgetCategory.HOUSING.value == "housing"
    assert BudgetCategory.FOOD.value == "food"
    assert BudgetCategory.TRANSPORT.value == "transport"
    assert BudgetCategory.EDUCATION.value == "education"
    assert BudgetCategory.HEALTH.value == "health"
    assert BudgetCategory.OTHER.value == "other"
