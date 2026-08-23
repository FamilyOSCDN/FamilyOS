"""Canonical build-toolchain policy models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolchainDistributionRequirement:
    """Compatibility requirement for one critical toolchain distribution."""

    distribution: str
    requirement: str

    def __post_init__(self) -> None:
        """Reject incomplete distribution requirements."""

        if not self.distribution:
            raise ValueError(
                "toolchain policy distribution must not be empty",
            )


@dataclass(frozen=True, slots=True)
class ToolchainPolicy:
    """Canonical compatibility policy for one package-build toolchain."""

    runtime_requirement: str
    distribution_requirements: tuple[
        ToolchainDistributionRequirement,
        ...,
    ]

    def __post_init__(self) -> None:
        """Reject incomplete or ambiguous toolchain policy."""

        if not self.runtime_requirement:
            raise ValueError(
                "toolchain runtime requirement must not be empty",
            )

        if not self.distribution_requirements:
            raise ValueError(
                "toolchain distribution requirements must not be empty",
            )

        distributions = tuple(
            item.distribution
            for item in self.distribution_requirements
        )

        if len(distributions) != len(set(distributions)):
            raise ValueError(
                "toolchain policy distributions must be unique",
            )

    @property
    def requirements_by_distribution(self) -> dict[str, str]:
        """Return deterministic requirements keyed by distribution."""

        return {
            item.distribution: item.requirement
            for item in self.distribution_requirements
        }
