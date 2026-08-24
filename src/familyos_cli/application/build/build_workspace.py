"""Canonical workspace model for build execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class BuildWorkspace:
    """Filesystem workspace owned by one canonical build execution."""

    root: Path
    staging_dir: Path
    intermediate_dir: Path

    def __post_init__(self) -> None:
        """Reject inconsistent canonical workspace layouts."""

        if not self.root.is_absolute():
            raise ValueError("workspace root must be absolute")

        if self.staging_dir != self.root / "staging":
            raise ValueError(
                "workspace staging directory must be rooted at workspace root"
            )

        if self.intermediate_dir != self.root / "intermediate":
            raise ValueError(
                "workspace intermediate directory must be rooted at workspace root"
            )
