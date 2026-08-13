from decimal import Decimal

import pytest

from familyos_cli.plugins.builtin.finance.liabilities.liability import (
    Liability,
)
from familyos_cli.plugins.builtin.finance.liabilities.liability_registry import (
    LiabilityRegistry,
)
from familyos_cli.plugins.builtin.finance.liabilities.liability_type import (
    LiabilityType,
)


def create_liability(
    liability_id: str = "liability-001",
) -> Liability:
    return Liability(
        id=liability_id,
        owner_id="family-001",
        name="Mortgage",
        type=LiabilityType.MORTGAGE,
        amount=Decimal("50000"),
        currency="EUR",
    )


def test_liability_registry_adds_liabilities() -> None:
    registry = LiabilityRegistry()

    registry.add(
        create_liability(),
    )

    assert len(
        registry.list(),
    ) == 1


def test_liability_registry_gets_by_id() -> None:
    registry = LiabilityRegistry()

    registry.add(
        create_liability(),
    )

    liability = registry.get(
        "liability-001",
    )

    assert liability is not None
    assert liability.id == "liability-001"


def test_liability_registry_returns_none_for_unknown_id() -> None:
    registry = LiabilityRegistry()

    assert registry.get(
        "unknown",
    ) is None


def test_liability_registry_rejects_duplicate_id() -> None:
    registry = LiabilityRegistry()

    liability = create_liability()

    registry.add(
        liability,
    )

    with pytest.raises(
        ValueError,
        match="Liability 'liability-001' already exists",
    ):
        registry.add(
            create_liability(),
        )

    assert registry.list() == [
        liability,
    ]
