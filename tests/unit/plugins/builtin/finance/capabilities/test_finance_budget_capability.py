from familyos_cli.plugins.builtin.finance.capabilities.finance_budget_capability import (
    FinanceBudgetCapability,
)


def test_finance_budget_capability_has_expected_identifier() -> None:
    capability = FinanceBudgetCapability.create()

    assert str(
        capability.id,
    ) == "familyos.finance.budget"


def test_finance_budget_capability_has_finance_metadata() -> None:
    capability = FinanceBudgetCapability.create()

    assert capability.display_name == "Finance Budget"
    assert capability.metadata["domain"] == "finance"
    assert capability.metadata["version"] == "1.0.0"
