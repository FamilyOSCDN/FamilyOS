"""Tests for canonical build-toolchain policy models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.application.build.toolchain_policy import (
    ToolchainDistributionRequirement,
    ToolchainPolicy,
)


def _policy() -> ToolchainPolicy:
    return ToolchainPolicy(
        runtime_requirement=">=3.13,<3.14",
        distribution_requirements=(
            ToolchainDistributionRequirement(
                distribution="build",
                requirement=">=1.5",
            ),
            ToolchainDistributionRequirement(
                distribution="wheel",
                requirement="",
            ),
        ),
    )


def test_policy_preserves_runtime_and_distribution_requirements() -> None:
    policy = _policy()

    assert policy.runtime_requirement == ">=3.13,<3.14"
    assert policy.requirements_by_distribution == {
        "build": ">=1.5",
        "wheel": "",
    }


def test_distribution_requirement_rejects_empty_distribution() -> None:
    with pytest.raises(
        ValueError,
        match="toolchain policy distribution must not be empty",
    ):
        ToolchainDistributionRequirement(
            distribution="",
            requirement=">=1",
        )


def test_policy_rejects_empty_runtime_requirement() -> None:
    with pytest.raises(
        ValueError,
        match="toolchain runtime requirement must not be empty",
    ):
        ToolchainPolicy(
            runtime_requirement="",
            distribution_requirements=(
                ToolchainDistributionRequirement(
                    distribution="build",
                    requirement=">=1.5",
                ),
            ),
        )


def test_policy_rejects_empty_distribution_requirements() -> None:
    with pytest.raises(
        ValueError,
        match="toolchain distribution requirements must not be empty",
    ):
        ToolchainPolicy(
            runtime_requirement=">=3.13,<3.14",
            distribution_requirements=(),
        )


def test_policy_rejects_duplicate_distributions() -> None:
    requirement = ToolchainDistributionRequirement(
        distribution="build",
        requirement=">=1.5",
    )

    with pytest.raises(
        ValueError,
        match="toolchain policy distributions must be unique",
    ):
        ToolchainPolicy(
            runtime_requirement=">=3.13,<3.14",
            distribution_requirements=(
                requirement,
                requirement,
            ),
        )


def test_policy_is_immutable() -> None:
    policy = _policy()

    with pytest.raises(FrozenInstanceError):
        policy.runtime_requirement = ">=3.14"  # type: ignore[misc]
