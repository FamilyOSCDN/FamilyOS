"""Immutable canonical Testing Framework evidence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.testing.test_execution_id import TestExecutionId
from familyos_cli.application.testing.test_execution_result import (
    TestExecutionResult,
)


@dataclass(frozen=True, slots=True)
class TestingEvidence:
    """Evidence associated with one canonical test execution."""

    execution_id: TestExecutionId
    source_revision: str
    result: TestExecutionResult
    captured_at: datetime

    def __post_init__(self) -> None:
        """Reject incomplete canonical testing evidence."""

        if not self.source_revision:
            raise ValueError(
                "Testing Evidence requires a source revision"
            )

        if (
            self.captured_at.tzinfo is None
            or self.captured_at.utcoffset() is None
        ):
            raise ValueError(
                "Testing Evidence timestamp must be timezone-aware"
            )
