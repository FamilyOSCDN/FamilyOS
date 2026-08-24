"""Port for observing source state for canonical test execution."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.testing.testing_source_state import (
    TestingSourceState,
)


class TestingSourceStateProviderPort(ABC):
    """Observe repository source state without exposing infrastructure details."""

    @abstractmethod
    def observe(
        self,
        *,
        project_root: Path,
    ) -> TestingSourceState:
        """Return source state observable for the exact project root."""

        raise NotImplementedError
