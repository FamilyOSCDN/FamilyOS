"""Protocol defining the data required for cycle detection."""

from __future__ import annotations

from typing import Protocol


class CycleDetectionSource(Protocol):
    """Provide dependency graph access for cycle detection."""

    def plugins(self) -> tuple[str, ...]:
        """Return all plugins available in the graph."""

    def dependencies_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        """Return direct dependencies of a plugin."""
