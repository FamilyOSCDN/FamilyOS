"""Port for canonical Testing Framework execution with evidence."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.testing.testing_evidence import TestingEvidence


class TestingExecutionPort(ABC):
    """Execute canonical tests and return Testing-owned evidence."""

    @abstractmethod
    def execute(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> TestingEvidence:
        """Execute selected tests and return their canonical evidence."""

        raise NotImplementedError
