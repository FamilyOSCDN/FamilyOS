"""Conflict detection service."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.conflicts import (
    PluginConflict,
)
from familyos_cli.plugins.ecosystem.diagnostics.ports import (
    ConflictDetectionSource,
)


class ConflictDetector:
    """Detect plugin resolution conflicts."""

    def __init__(
        self,
        source: ConflictDetectionSource,
    ) -> None:
        """Initialize the detector."""

        self._source = source

    def detect(self) -> tuple[PluginConflict, ...]:
        """Detect conflicts.

        The detection algorithm will be implemented in Sprint AC.4B.
        """

        return ()
