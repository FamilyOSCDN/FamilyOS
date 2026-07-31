"""Protocol defining the data required for conflict detection."""

from __future__ import annotations

from typing import Protocol


class ConflictDetectionSource(Protocol):
    """Provide dependency information required by the conflict detector."""

    def plugins(self) -> tuple[str, ...]:
        """Return all plugins participating in the resolution."""

    def candidate_versions(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        """Return candidate versions for a plugin."""

    def constraints_for(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        """Return all version constraints for a plugin."""

    def dependents_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        """Return plugins depending on the given plugin."""
