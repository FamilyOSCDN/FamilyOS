"""Port for observing source state before canonical package construction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.build.source_state import SourceState


class SourceStateProviderPort(ABC):
    """Observe repository source state without exposing infrastructure details."""

    @abstractmethod
    def observe(self, *, project_root: Path) -> SourceState:
        """Return the source state observable for the exact project root."""

        raise NotImplementedError
