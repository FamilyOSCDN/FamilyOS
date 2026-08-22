"""Immutable dependency state captured for canonical build execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DependencyState:
    """Identity of canonical dependency declaration and locked state."""

    declaration_path: Path
    declaration_digest: str
    lock_path: Path
    lock_digest: str

    def __post_init__(self) -> None:
        """Reject incomplete dependency-state identities."""

        if not self.declaration_digest:
            raise ValueError("dependency declaration digest must not be empty")

        if not self.lock_digest:
            raise ValueError("dependency lock digest must not be empty")
