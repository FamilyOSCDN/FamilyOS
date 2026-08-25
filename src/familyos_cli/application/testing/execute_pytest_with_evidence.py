"""Execute pytest and produce canonical Testing Evidence."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.testing.pytest_runner import (
    PytestRunnerPort,
)
from familyos_cli.application.ports.testing.testing_evidence_producer import (
    TestingEvidenceProducerPort,
)
from familyos_cli.application.ports.testing.testing_execution import (
    TestingExecutionPort,
)
from familyos_cli.application.testing.pytest_result_normalizer import (
    PytestResultNormalizer,
)
from familyos_cli.application.testing.testing_evidence import (
    TestingEvidence,
)


class ExecutePytestWithEvidenceUseCase(TestingExecutionPort):
    """Execute pytest, normalize its result, and produce Testing Evidence."""

    def __init__(
        self,
        *,
        runner: PytestRunnerPort,
        normalizer: PytestResultNormalizer,
        evidence_producer: TestingEvidenceProducerPort,
    ) -> None:
        self._runner = runner
        self._normalizer = normalizer
        self._evidence_producer = evidence_producer

    def execute(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> TestingEvidence:
        """Execute selected pytest tests and return canonical Testing Evidence."""

        native_result = self._runner.run(
            project_root=project_root,
            test_paths=test_paths,
        )

        canonical_result = self._normalizer.normalize(
            native_result,
        )

        return self._evidence_producer.execute(
            project_root=project_root,
            result=canonical_result,
            native_exit_code=native_result.exit_code,
        )
