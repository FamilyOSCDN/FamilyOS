"""Port for structured pytest execution."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.testing import PytestExecutionResult


class PytestRunnerPort(ABC):
    """Execute pytest and return a structured runner-specific result."""

    @abstractmethod
    def run(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> PytestExecutionResult:
        """Execute selected pytest paths and return structured results."""

        raise NotImplementedError
