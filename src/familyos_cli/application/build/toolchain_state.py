"""Immutable critical toolchain state for canonical build execution."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolchainVersion:
    """Installed version of one critical build-tool distribution."""

    distribution: str
    version: str

    def __post_init__(self) -> None:
        """Reject incomplete toolchain identities."""

        if not self.distribution:
            raise ValueError("toolchain distribution must not be empty")

        if not self.version:
            raise ValueError("toolchain version must not be empty")


@dataclass(frozen=True, slots=True)
class ToolchainState:
    """Critical tool versions observed for one canonical build."""

    critical_versions: tuple[ToolchainVersion, ...]

    def __post_init__(self) -> None:
        """Reject empty or ambiguous critical toolchain state."""

        if not self.critical_versions:
            raise ValueError("critical toolchain versions must not be empty")

        distributions = tuple(
            component.distribution for component in self.critical_versions
        )
        if len(set(distributions)) != len(distributions):
            raise ValueError(
                "critical toolchain distributions must be unique",
            )
