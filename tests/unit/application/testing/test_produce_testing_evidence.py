"""Tests for canonical Testing Evidence production orchestration."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from familyos_cli.application.ports.testing import (
    TestingClockPort,
    TestingSourceStateProviderPort,
)
from familyos_cli.application.testing import (
    TestExecutionResult as CanonicalExecutionResult,
)
from familyos_cli.application.testing import (
    TestExecutionStatus as CanonicalExecutionStatus,
)
from familyos_cli.application.testing import (
    TestExecutionSummary as CanonicalExecutionSummary,
)
from familyos_cli.application.testing import (
    TestingSourceState as CanonicalTestingSourceState,
)
from familyos_cli.application.testing.produce_testing_evidence import (
    ProduceTestingEvidenceUseCase,
)


class _RecordingSourceStateProvider(
    TestingSourceStateProviderPort
):
    def __init__(
        self,
        state: CanonicalTestingSourceState,
    ) -> None:
        self.state = state
        self.calls: list[Path] = []

    def observe(
        self,
        *,
        project_root: Path,
    ) -> CanonicalTestingSourceState:
        self.calls.append(project_root)
        return self.state


class _RecordingClock(TestingClockPort):
    def __init__(
        self,
        current: datetime,
    ) -> None:
        self.current = current
        self.calls = 0

    def now(self) -> datetime:
        self.calls += 1
        return self.current


def _result() -> CanonicalExecutionResult:
    return CanonicalExecutionResult(
        status=CanonicalExecutionStatus.PASSED,
        summary=CanonicalExecutionSummary(
            discovered=3,
            executed=3,
            passed=3,
            failed=0,
            skipped=0,
            errors=0,
            duration_seconds=0.25,
        ),
    )


def test_use_case_observes_exact_project_root(
    tmp_path: Path,
) -> None:
    provider = _RecordingSourceStateProvider(
        CanonicalTestingSourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        )
    )

    use_case = ProduceTestingEvidenceUseCase(
        source_state_provider=provider,
        clock=_RecordingClock(
            datetime(2026, 8, 24, 19, 45, tzinfo=UTC)
        ),
    )

    use_case.execute(
        project_root=tmp_path,
        result=_result(),
    )

    assert provider.calls == [tmp_path]


def test_use_case_captures_clock_once(
    tmp_path: Path,
) -> None:
    clock = _RecordingClock(
        datetime(2026, 8, 24, 19, 45, tzinfo=UTC)
    )

    use_case = ProduceTestingEvidenceUseCase(
        source_state_provider=_RecordingSourceStateProvider(
            CanonicalTestingSourceState(
                revision="0123456789abcdef0123456789abcdef01234567",
                dirty=False,
            )
        ),
        clock=clock,
    )

    evidence = use_case.execute(
        project_root=tmp_path,
        result=_result(),
    )

    assert clock.calls == 1
    assert evidence.captured_at == clock.current


def test_use_case_preserves_canonical_result(
    tmp_path: Path,
) -> None:
    result = _result()

    use_case = ProduceTestingEvidenceUseCase(
        source_state_provider=_RecordingSourceStateProvider(
            CanonicalTestingSourceState(
                revision="0123456789abcdef0123456789abcdef01234567",
                dirty=False,
            )
        ),
        clock=_RecordingClock(
            datetime(2026, 8, 24, 19, 45, tzinfo=UTC)
        ),
    )

    evidence = use_case.execute(
        project_root=tmp_path,
        result=result,
    )

    assert evidence.result is result


def test_use_case_generates_distinct_execution_identity(
    tmp_path: Path,
) -> None:
    use_case = ProduceTestingEvidenceUseCase(
        source_state_provider=_RecordingSourceStateProvider(
            CanonicalTestingSourceState(
                revision="0123456789abcdef0123456789abcdef01234567",
                dirty=False,
            )
        ),
        clock=_RecordingClock(
            datetime(2026, 8, 24, 19, 45, tzinfo=UTC)
        ),
    )

    first = use_case.execute(
        project_root=tmp_path,
        result=_result(),
    )
    second = use_case.execute(
        project_root=tmp_path,
        result=_result(),
    )

    assert first.execution_id != second.execution_id


def test_use_case_rejects_missing_source_revision(
    tmp_path: Path,
) -> None:
    use_case = ProduceTestingEvidenceUseCase(
        source_state_provider=_RecordingSourceStateProvider(
            CanonicalTestingSourceState(
                revision=None,
                dirty=None,
            )
        ),
        clock=_RecordingClock(
            datetime(2026, 8, 24, 19, 45, tzinfo=UTC)
        ),
    )

    with pytest.raises(
        ValueError,
        match="testing source state does not contain a captured source revision",
    ):
        use_case.execute(
            project_root=tmp_path,
            result=_result(),
        )
