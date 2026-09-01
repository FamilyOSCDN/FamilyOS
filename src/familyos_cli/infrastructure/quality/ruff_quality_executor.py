"""Ruff-backed implementation of the canonical Quality executor port."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityRule,
    QualityStatus,
    QualityTarget,
)

_TIMEOUT_SECONDS = 120
_STATIC_ANALYSIS = QualityEvidenceType("STATIC_ANALYSIS")


class RuffQualityExecutor(QualityExecutorPort):
    """Execute a governed Ruff check and normalize it into Quality models."""

    def __init__(
        self,
        *,
        finding_id_factory: Callable[[], QualityFindingId],
        evidence_id_factory: Callable[[], QualityEvidenceId],
        clock: Callable[[], datetime] | None = None,
        monotonic_clock: Callable[[], float] | None = None,
        python_executable: str | None = None,
        timeout_seconds: int = _TIMEOUT_SECONDS,
    ) -> None:
        self._finding_id_factory = finding_id_factory
        self._evidence_id_factory = evidence_id_factory
        self._clock = clock or (lambda: datetime.now(UTC))
        self._monotonic_clock = monotonic_clock or time.monotonic
        self._python_executable = python_executable or sys.executable
        self._timeout_seconds = timeout_seconds

    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        started = self._monotonic_clock()
        target_path = target.path

        if target_path is None:
            return self._result_without_execution(
                check_id=check_id,
                started=started,
                diagnostic="Ruff Quality target requires QualityTarget.path",
            )

        version, version_diagnostic = self._collect_version()

        try:
            completed = subprocess.run(
                [
                    self._python_executable,
                    "-m",
                    "ruff",
                    "check",
                    str(Path(target_path)),
                    "--output-format=json",
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return self._execution_error_result(
                check_id=check_id,
                rule=rule,
                target=target,
                started=started,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic="Ruff execution timed out",
                metadata=(("error_kind", "timeout"),),
            )
        except OSError as exc:
            return self._execution_error_result(
                check_id=check_id,
                rule=rule,
                target=target,
                started=started,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic=f"Ruff execution failed: {exc}",
                metadata=(("error_kind", "process_failure"),),
            )

        duration = self._duration(started)

        if completed.returncode not in (0, 1):
            diagnostic = self._process_diagnostic(
                "Ruff execution returned an unexpected exit status",
                completed.returncode,
                completed.stderr,
            )
            return self._execution_error_result_with_duration(
                check_id=check_id,
                rule=rule,
                target=target,
                duration=duration,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic=diagnostic,
                metadata=(
                    ("error_kind", "unexpected_exit"),
                    ("exit_code", str(completed.returncode)),
                ),
            )

        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            return self._execution_error_result_with_duration(
                check_id=check_id,
                rule=rule,
                target=target,
                duration=duration,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic=f"Ruff returned invalid JSON: {exc.msg}",
                metadata=(
                    ("error_kind", "invalid_json"),
                    ("exit_code", str(completed.returncode)),
                ),
            )

        if not isinstance(payload, list):
            return self._execution_error_result_with_duration(
                check_id=check_id,
                rule=rule,
                target=target,
                duration=duration,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic="Ruff JSON output must be a list",
                metadata=(
                    ("error_kind", "invalid_json_shape"),
                    ("exit_code", str(completed.returncode)),
                ),
            )

        if completed.returncode == 0 and payload:
            return self._execution_error_result_with_duration(
                check_id=check_id,
                rule=rule,
                target=target,
                duration=duration,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic="Ruff exit status 0 returned violations",
                metadata=(
                    ("error_kind", "inconsistent_result"),
                    ("exit_code", "0"),
                ),
            )

        if completed.returncode == 1 and not payload:
            return self._execution_error_result_with_duration(
                check_id=check_id,
                rule=rule,
                target=target,
                duration=duration,
                version=version,
                version_diagnostic=version_diagnostic,
                diagnostic="Ruff exit status 1 returned no violations",
                metadata=(
                    ("error_kind", "inconsistent_result"),
                    ("exit_code", "1"),
                ),
            )

        evidence_id = self._evidence_id_factory()
        status = QualityStatus.PASS if completed.returncode == 0 else QualityStatus.FAIL
        evidence_result = (
            QualityEvidenceResult.PASS
            if status is QualityStatus.PASS
            else QualityEvidenceResult.FAIL
        )

        findings: list[QualityFinding] = []
        ruff_codes: list[str] = []
        for violation in payload:
            if not isinstance(violation, dict):
                return self._execution_error_result_with_duration(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    duration=duration,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    diagnostic="Ruff violation entries must be objects",
                    evidence_id=evidence_id,
                    metadata=(
                        ("error_kind", "invalid_violation"),
                        ("exit_code", str(completed.returncode)),
                    ),
                )
            try:
                finding, ruff_code = self._finding_from_violation(
                    violation=violation,
                    rule=rule,
                    target=target,
                    evidence_id=evidence_id,
                )
            except (KeyError, TypeError, ValueError) as exc:
                return self._execution_error_result_with_duration(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    duration=duration,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    diagnostic=f"Ruff violation payload is invalid: {exc}",
                    evidence_id=evidence_id,
                    metadata=(
                        ("error_kind", "invalid_violation"),
                        ("exit_code", str(completed.returncode)),
                    ),
                )
            findings.append(finding)
            ruff_codes.append(ruff_code)

        evidence = self._evidence(
            evidence_id=evidence_id,
            rule=rule,
            target=target,
            result=evidence_result,
            version=version,
            metadata=(
                ("exit_code", str(completed.returncode)),
                ("violation_count", str(len(findings))),
                ("ruff_codes", json.dumps(ruff_codes, separators=(",", ":"))),
            ),
        )

        return QualityCheckResult(
            check_id=check_id,
            status=status,
            findings=tuple(findings),
            evidence=(evidence,),
            duration_seconds=duration,
            diagnostics=self._diagnostics(version_diagnostic),
        )

    def _collect_version(self) -> tuple[str | None, str | None]:
        try:
            completed = subprocess.run(
                [self._python_executable, "-m", "ruff", "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None, "Ruff version unavailable"

        if completed.returncode != 0:
            return None, "Ruff version unavailable"

        version = completed.stdout.strip()
        if not version:
            return None, "Ruff version unavailable"
        return version, None

    def _finding_from_violation(
        self,
        *,
        violation: dict[str, Any],
        rule: QualityRule,
        target: QualityTarget,
        evidence_id: QualityEvidenceId,
    ) -> tuple[QualityFinding, str]:
        code = violation["code"]
        message = violation["message"]
        filename = violation["filename"]
        location = violation["location"]

        if not isinstance(code, str) or not code:
            raise ValueError("code must be a non-empty string")
        if not isinstance(message, str) or not message:
            raise ValueError("message must be a non-empty string")
        if not isinstance(filename, str) or not filename:
            raise ValueError("filename must be a non-empty string")
        if not isinstance(location, dict):
            raise TypeError("location must be an object")

        row = location["row"]
        column = location["column"]
        if isinstance(row, bool) or not isinstance(row, int):
            raise TypeError("location row must be an integer")
        if isinstance(column, bool) or not isinstance(column, int):
            raise TypeError("location column must be an integer")

        finding = QualityFinding(
            id=self._finding_id_factory(),
            rule_id=rule.id,
            domain=rule.domain,
            severity=rule.severity,
            status=QualityStatus.FAIL,
            message=message,
            target=target,
            location=f"{filename}:{row}:{column}",
            evidence_ids=(str(evidence_id),),
        )
        return finding, code

    def _evidence(
        self,
        *,
        evidence_id: QualityEvidenceId,
        rule: QualityRule,
        target: QualityTarget,
        result: QualityEvidenceResult,
        version: str | None,
        metadata: tuple[tuple[str, str], ...],
    ) -> QualityEvidence:
        return QualityEvidence(
            id=evidence_id,
            type=_STATIC_ANALYSIS,
            source="quality.ruff",
            target=target,
            result=result,
            created_at=self._clock(),
            revision=None,
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            tool="ruff",
            tool_version=version,
            metadata=metadata,
            artifact=None,
        )

    def _execution_error_result(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
        started: float,
        version: str | None,
        version_diagnostic: str | None,
        diagnostic: str,
        metadata: tuple[tuple[str, str], ...],
    ) -> QualityCheckResult:
        return self._execution_error_result_with_duration(
            check_id=check_id,
            rule=rule,
            target=target,
            duration=self._duration(started),
            version=version,
            version_diagnostic=version_diagnostic,
            diagnostic=diagnostic,
            metadata=metadata,
        )

    def _execution_error_result_with_duration(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
        duration: float,
        version: str | None,
        version_diagnostic: str | None,
        diagnostic: str,
        metadata: tuple[tuple[str, str], ...],
        evidence_id: QualityEvidenceId | None = None,
    ) -> QualityCheckResult:
        error_evidence_id = evidence_id or self._evidence_id_factory()
        evidence = self._evidence(
            evidence_id=error_evidence_id,
            rule=rule,
            target=target,
            result=QualityEvidenceResult.ERROR,
            version=version,
            metadata=metadata,
        )
        return QualityCheckResult(
            check_id=check_id,
            status=QualityStatus.ERROR,
            evidence=(evidence,),
            duration_seconds=duration,
            diagnostics=self._diagnostics(version_diagnostic, diagnostic),
        )

    def _result_without_execution(
        self,
        *,
        check_id: QualityCheckId,
        started: float,
        diagnostic: str,
    ) -> QualityCheckResult:
        return QualityCheckResult(
            check_id=check_id,
            status=QualityStatus.ERROR,
            duration_seconds=self._duration(started),
            diagnostics=(diagnostic,),
        )

    def _duration(self, started: float) -> float:
        return max(0.0, self._monotonic_clock() - started)

    @staticmethod
    def _diagnostics(*values: str | None) -> tuple[str, ...]:
        return tuple(value for value in values if value is not None)

    @staticmethod
    def _process_diagnostic(prefix: str, returncode: int, stderr: str) -> str:
        stderr_text = stderr.strip()
        if stderr_text:
            return f"{prefix} {returncode}: {stderr_text}"
        return f"{prefix} {returncode}"
