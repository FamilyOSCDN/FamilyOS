"""Pytest plugin producing structured FamilyOS execution results."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest


@dataclass(slots=True)
class _NodeOutcome:
    setup: str | None = None
    call: str | None = None
    teardown: str | None = None


@dataclass(slots=True)
class FamilyOSPytestResultPlugin:
    """Collect pytest lifecycle reports into one terminal outcome per node."""

    result_path: Path
    discovered: int = 0
    started_at: float = field(default_factory=time.monotonic)
    outcomes: dict[str, _NodeOutcome] = field(default_factory=dict)

    def pytest_collection_finish(
        self,
        session: pytest.Session,
    ) -> None:
        """Record the number of collected tests."""

        self.discovered = len(session.items)

    def pytest_runtest_logreport(
        self,
        report: pytest.TestReport,
    ) -> None:
        """Record one pytest phase without double-counting one test node."""

        outcome = self.outcomes.setdefault(
            report.nodeid,
            _NodeOutcome(),
        )

        value = self._report_state(report)

        if report.when == "setup":
            outcome.setup = value
        elif report.when == "call":
            outcome.call = value
        elif report.when == "teardown":
            outcome.teardown = value

    def pytest_sessionfinish(
        self,
        session: pytest.Session,
        exitstatus: int | pytest.ExitCode,
    ) -> None:
        """Write the final structured execution result."""

        counts = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
        }

        for outcome in self.outcomes.values():
            counts[self._terminal_state(outcome)] += 1

        payload: dict[str, Any] = {
            "exit_code": int(exitstatus),
            "discovered": self.discovered,
            "executed": len(self.outcomes),
            "passed": counts["passed"],
            "failed": counts["failed"],
            "skipped": counts["skipped"],
            "errors": counts["errors"],
            "duration_seconds": max(
                0.0,
                time.monotonic() - self.started_at,
            ),
        }

        self.result_path.write_text(
            json.dumps(payload, sort_keys=True),
            encoding="utf-8",
        )

    @staticmethod
    def _report_state(report: pytest.TestReport) -> str:
        if report.failed:
            return "failed"
        if report.skipped:
            return "skipped"
        return "passed"

    @staticmethod
    def _terminal_state(outcome: _NodeOutcome) -> str:
        if outcome.setup == "failed":
            return "errors"

        if outcome.teardown == "failed":
            return "errors"

        if outcome.call == "failed":
            return "failed"

        if outcome.setup == "skipped" or outcome.call == "skipped":
            return "skipped"

        if outcome.call == "passed":
            return "passed"

        return "errors"

def pytest_configure(config: pytest.Config) -> None:
    """Register the FamilyOS structured-result collector."""

    result_path = os.environ.get(
        "FAMILYOS_PYTEST_RESULT_PATH"
    )

    if not result_path:
        return

    plugin = FamilyOSPytestResultPlugin(
        result_path=Path(result_path).resolve(),
    )

    config.pluginmanager.register(
        plugin,
        "familyos-structured-result",
    )
