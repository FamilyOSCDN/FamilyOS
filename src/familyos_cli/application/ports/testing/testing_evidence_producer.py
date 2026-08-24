"""Port for producing canonical Testing Evidence."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.testing.test_execution_result import (
    TestExecutionResult,
)
from familyos_cli.application.testing.testing_evidence import TestingEvidence


class TestingEvidenceProducerPort(ABC):
    """Produce canonical evidence from an established Testing result."""

    @abstractmethod
    def execute(
        self,
        *,
        project_root: Path,
        result: TestExecutionResult,
    ) -> TestingEvidence:
        """Produce canonical Testing Evidence for one execution."""

        raise NotImplementedError
