"""Canonical staged build-input contract."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class StagedBuildInputs:
    """Represent the materialized inputs of one staged package build."""

    project_root: Path

    def __post_init__(self) -> None:
        """Reject invalid staged-project roots."""

        if not self.project_root.is_absolute():
            raise ValueError("staged project root must be absolute")
