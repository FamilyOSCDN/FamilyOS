"""Evaluate canonical Testing Evidence against current source state."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.testing.testing_evidence_freshness import (
    TestingEvidenceFreshnessPort,
)
from familyos_cli.application.ports.testing.testing_source_state_provider import (
    TestingSourceStateProviderPort,
)
from familyos_cli.application.testing.testing_evidence import TestingEvidence
from familyos_cli.application.testing.testing_evidence_freshness import (
    TestingEvidenceFreshness,
    TestingEvidenceFreshnessEvaluator,
)


class EvaluateTestingEvidenceFreshnessUseCase(
    TestingEvidenceFreshnessPort
):
    """Evaluate Testing Evidence using Testing-owned source authority."""

    def __init__(
        self,
        *,
        source_state_provider: TestingSourceStateProviderPort,
        evaluator: TestingEvidenceFreshnessEvaluator | None = None,
    ) -> None:
        self._source_state_provider = source_state_provider
        self._evaluator = (
            evaluator or TestingEvidenceFreshnessEvaluator()
        )

    def evaluate(
        self,
        *,
        project_root: Path,
        evidence: TestingEvidence,
    ) -> TestingEvidenceFreshness:
        """Compare evidence with the current project source state."""

        current_source_state = self._source_state_provider.observe(
            project_root=project_root,
        )

        return self._evaluator.evaluate(
            evidence=evidence,
            current_source_state=current_source_state,
        )
