"""Produce canonical Testing Evidence from established authorities."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.testing.testing_clock import (
    TestingClockPort,
)
from familyos_cli.application.ports.testing.testing_evidence_producer import (
    TestingEvidenceProducerPort,
)
from familyos_cli.application.ports.testing.testing_source_state_provider import (
    TestingSourceStateProviderPort,
)
from familyos_cli.application.testing.test_execution_id import TestExecutionId
from familyos_cli.application.testing.test_execution_result import (
    TestExecutionResult,
)
from familyos_cli.application.testing.testing_evidence import TestingEvidence
from familyos_cli.application.testing.testing_evidence_factory import (
    TestingEvidenceFactory,
)


class ProduceTestingEvidenceUseCase(TestingEvidenceProducerPort):
    """Orchestrate canonical Testing Evidence production."""

    def __init__(
        self,
        *,
        source_state_provider: TestingSourceStateProviderPort,
        clock: TestingClockPort,
        evidence_factory: TestingEvidenceFactory | None = None,
    ) -> None:
        self._source_state_provider = source_state_provider
        self._clock = clock
        self._evidence_factory = (
            evidence_factory or TestingEvidenceFactory()
        )

    def execute(
        self,
        *,
        project_root: Path,
        result: TestExecutionResult,
        native_exit_code: int | None = None,
    ) -> TestingEvidence:
        """Produce evidence for one established canonical test result."""

        source_state = self._source_state_provider.observe(
            project_root=project_root,
        )
        captured_at = self._clock.now()
        execution_id = TestExecutionId.generate()

        return self._evidence_factory.create(
            execution_id=execution_id,
            source_state=source_state,
            result=result,
            captured_at=captured_at,
            native_exit_code=native_exit_code,
        )
