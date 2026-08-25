"""Construct canonical Testing Evidence from established authorities."""

from __future__ import annotations

from datetime import datetime

from familyos_cli.application.testing.test_execution_id import TestExecutionId
from familyos_cli.application.testing.test_execution_result import (
    TestExecutionResult,
)
from familyos_cli.application.testing.testing_evidence import TestingEvidence
from familyos_cli.application.testing.testing_source_state import (
    TestingSourceState,
)


class TestingEvidenceFactory:
    """Assemble Testing Evidence without recalculating canonical authorities."""

    def create(
        self,
        *,
        execution_id: TestExecutionId,
        source_state: TestingSourceState,
        result: TestExecutionResult,
        captured_at: datetime,
        native_exit_code: int | None = None,
    ) -> TestingEvidence:
        """Build canonical evidence from one established test execution."""

        if source_state.revision is None:
            raise ValueError(
                "testing source state does not contain a captured source revision"
            )

        if source_state.dirty is None:
            raise ValueError(
                "testing source state does not contain a captured dirty state"
            )

        return TestingEvidence(
            execution_id=execution_id,
            source_revision=source_state.revision,
            source_dirty=source_state.dirty,
            result=result,
            captured_at=captured_at,
            native_exit_code=native_exit_code,
        )
