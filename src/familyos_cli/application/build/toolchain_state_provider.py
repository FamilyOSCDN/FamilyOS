"""Capture installed critical toolchain versions for canonical builds."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version

from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)

_CRITICAL_DISTRIBUTIONS = (
    "build",
    "pip-tools",
    "setuptools",
    "wheel",
)


class ToolchainStateProvider:
    """Observe the installed canonical package-build toolchain."""

    def capture(self) -> ToolchainState:
        """Capture critical tool identities in deterministic order."""

        try:
            versions = tuple(
                ToolchainVersion(
                    distribution=distribution,
                    version=distribution_version(distribution),
                )
                for distribution in _CRITICAL_DISTRIBUTIONS
            )
        except PackageNotFoundError as error:
            missing = error.name or "unknown"
            raise ValueError(
                f"critical toolchain distribution {missing!r} is unavailable",
            ) from error

        return ToolchainState(critical_versions=versions)
