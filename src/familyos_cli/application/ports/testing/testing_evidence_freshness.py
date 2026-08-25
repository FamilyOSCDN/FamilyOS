"""Port for evaluating canonical Testing Evidence freshness."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.testing.testing_evidence import TestingEvidence
from familyos_cli.application.testing.testing_evidence_freshness import (
    TestingEvidenceFreshness,
)


class TestingEvidenceFreshnessPort(ABC):
    """Evaluate Testing Evidence against the current project source state."""

    @abstractmethod
    def evaluate(
        self,
        *,
        project_root: Path,
        evidence: TestingEvidence,
    ) -> TestingEvidenceFreshness:
        """Return canonical freshness for Testing Evidence."""

        raise NotImplementedError
