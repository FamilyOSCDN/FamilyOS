from decimal import Decimal

from pytest import raises

from familyos_cli.plugins.builtin.finance.liabilities.liability import (
    Liability,
)
from familyos_cli.plugins.builtin.finance.liabilities.liability_type import (
    LiabilityType,
)


def create_liability(
    amount: Decimal = Decimal("50000"),
    liability_id: str = "liability-001",
) -> Liability:
    return Liability(
        id=liability_id,
        owner_id="family-001",
        name="Home Mortgage",
        type=LiabilityType.MORTGAGE,
        amount=amount,
        currency="EUR",
    )


def test_liability_can_be_created() -> None:
    liability = create_liability()

    assert liability.id == "liability-001"
    assert liability.type == LiabilityType.MORTGAGE
    assert liability.amount == Decimal("50000")


def test_liability_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Liability id cannot be empty.",
    ):
        create_liability(
            liability_id="",
        )


def test_liability_rejects_empty_owner_id() -> None:
    with raises(
        ValueError,
        match="Liability owner id cannot be empty.",
    ):
        Liability(
            id="liability-001",
            owner_id="",
            name="Mortgage",
            type=LiabilityType.MORTGAGE,
            amount=Decimal("50000"),
            currency="EUR",
        )


def test_liability_rejects_empty_name() -> None:
    with raises(
        ValueError,
        match="Liability name cannot be empty.",
    ):
        Liability(
            id="liability-001",
            owner_id="family-001",
            name="",
            type=LiabilityType.MORTGAGE,
            amount=Decimal("50000"),
            currency="EUR",
        )


def test_liability_rejects_non_positive_amount() -> None:
    with raises(
        ValueError,
        match="Liability amount must be positive.",
    ):
        create_liability(
            amount=Decimal("0"),
        )


def test_liability_rejects_empty_currency() -> None:
    with raises(
        ValueError,
        match="Liability currency cannot be empty.",
    ):
        Liability(
            id="liability-001",
            owner_id="family-001",
            name="Loan",
            type=LiabilityType.LOAN,
            amount=Decimal("1000"),
            currency="",
        )
