from familyos_cli.plugins.builtin.finance.liabilities.liability_type import (
    LiabilityType,
)


def test_liability_type_contains_expected_values() -> None:
    assert LiabilityType.MORTGAGE.value == "mortgage"
    assert LiabilityType.LOAN.value == "loan"
    assert LiabilityType.CREDIT.value == "credit"
