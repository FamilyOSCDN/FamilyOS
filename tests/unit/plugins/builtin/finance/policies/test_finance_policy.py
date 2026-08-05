"""Tests for FinancePolicy."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.finance.policies.finance_policy import (
    FinancePolicy,
)


def test_finance_policy_can_be_created() -> None:
    """Finance policy stores values."""

    policy = FinancePolicy(
        id="finance.policy.budget-control",
        name="Budget Control Policy",
        version="1.0.0",
        description="Controls family budget operations.",
    )

    assert policy.id == "finance.policy.budget-control"
    assert policy.name == "Budget Control Policy"
    assert policy.version == "1.0.0"
    assert policy.description == (
        "Controls family budget operations."
    )


def test_finance_policy_description_is_optional() -> None:
    """Description defaults to empty."""

    policy = FinancePolicy(
        id="finance.policy.basic",
        name="Basic Finance Policy",
        version="1.0.0",
    )

    assert policy.description == ""


def test_finance_policy_is_immutable() -> None:
    """Finance policies cannot be modified."""

    policy = FinancePolicy(
        id="finance.policy.basic",
        name="Basic Finance Policy",
        version="1.0.0",
    )

    with pytest.raises(FrozenInstanceError):
        policy.version = "2.0.0"  # type: ignore[misc]
