"""Immutable result model for canonical package-build execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class PackageBuildStatus(StrEnum):
    """Process-level outcome of package-build execution."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class PackageBuildResult:
    """Package outputs and diagnostics without artifact trust semantics."""

    status: PackageBuildStatus
    outputs: tuple[Path, ...] = ()
    exit_code: int | None = None
    diagnostic: str | None = None

    @property
    def successful(self) -> bool:
        """Return whether packaging completed successfully."""

        return self.status is PackageBuildStatus.SUCCEEDED
