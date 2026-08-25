"""Strict validation result for observed canonical source state."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceStateValidationResult:
    """Normalized source-state validation observations."""

    revision_identified: bool
    working_tree_clean: bool
    revision_diagnostic: str | None = None
    working_tree_diagnostic: str | None = None

    @property
    def successful(self) -> bool:
        """Return whether all strict source-state requirements passed."""

        return self.revision_identified and self.working_tree_clean
