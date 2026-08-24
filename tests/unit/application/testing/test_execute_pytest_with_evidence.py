"""Tests for canonical pytest execution with Testing Evidence."""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path

from familyos_cli.application.ports.testing import (
    PytestRunnerPort,
    TestingEvidenceProducerPort,
)
from familyos_cli.application.testing import (
    PytestExecutionResult,
    PytestResultNormalizer,
)
from familyos_cli.application.testing import (
    TestExecutionResult as CanonicalExecutionResult,
)
from familyos_cli.application.testing import (
    TestExecutionStatus as CanonicalExecutionStatus,
)
from familyos_cli.application.testing import (
    TestingEvidence as CanonicalTestingEvidence,
)
from familyos_cli.application.testing.execute_pytest_with_evidence import (
    ExecutePytestWithEvidenceUseCase,
)


class _Runner(PytestRunnerPort):
    def __init__(self) -> None:
        self.project_root: Path | None = None
        self.test_paths: tuple[Path, ...] | None = None

    def run(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> PytestExecutionResult:
        self.project_root = project_root
        self.test_paths = test_paths

        return PytestExecutionResult(
            exit_code=0,
            discovered=3,
            executed=3,
            passed=3,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=0.25,
        )


class _EvidenceProducer(TestingEvidenceProducerPort):
    def __init__(self) -> None:
        self.project_root: Path | None = None
        self.result: CanonicalExecutionResult | None = None

    def execute(
        self,
        *,
        project_root: Path,
        result: CanonicalExecutionResult,
    ) -> CanonicalTestingEvidence:
        self.project_root = project_root
        self.result = result

        raise RuntimeError("evidence boundary reached")


def test_execute_pytest_normalizes_before_producing_evidence(
    tmp_path: Path,
) -> None:
    runner = _Runner()
    producer = _EvidenceProducer()

    use_case = ExecutePytestWithEvidenceUseCase(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        evidence_producer=producer,
    )

    try:
        use_case.execute(
            project_root=tmp_path,
            test_paths=(),
        )
    except RuntimeError as exc:
        assert str(exc) == "evidence boundary reached"
    else:
        raise AssertionError("expected evidence boundary")

    assert runner.project_root == tmp_path
    assert runner.test_paths == ()

    assert producer.project_root == tmp_path
    assert producer.result is not None
    assert producer.result.status is CanonicalExecutionStatus.PASSED
    assert producer.result.summary.discovered == 3
    assert producer.result.summary.executed == 3
    assert producer.result.summary.passed == 3


def test_execute_pytest_preserves_selected_test_paths(
    tmp_path: Path,
) -> None:
    runner = _Runner()
    producer = _EvidenceProducer()

    use_case = ExecutePytestWithEvidenceUseCase(
        runner=runner,
        normalizer=PytestResultNormalizer(),
        evidence_producer=producer,
    )

    selected = (
        Path("tests/unit"),
        Path("tests/e2e"),
    )

    with suppress(RuntimeError):
        use_case.execute(
            project_root=tmp_path,
            test_paths=selected,
        )

    assert runner.test_paths == selected
