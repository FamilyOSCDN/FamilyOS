"""Pytest-backed implementation of the canonical Quality executor port."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

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
_TEST_EVIDENCE = QualityEvidenceType("TEST")


@dataclass(frozen=True, slots=True)
class _PytestCaseFailure:
    name: str
    message: str
    location: str | None


@dataclass(frozen=True, slots=True)
class _PytestReport:
    tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    failures: tuple[_PytestCaseFailure, ...]


class PytestQualityExecutor(QualityExecutorPort):
    """Execute a governed Pytest check and normalize it into Quality models."""

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

        if target.path is None:
            return QualityCheckResult(
                check_id=check_id,
                status=QualityStatus.ERROR,
                duration_seconds=self._duration(started),
                diagnostics=("Pytest Quality target requires QualityTarget.path",),
            )

        version, version_diagnostic = self._collect_version()

        with tempfile.TemporaryDirectory(prefix="familyos-quality-pytest-") as tmpdir:
            report_path = Path(tmpdir) / "pytest-junit.xml"
            command = [
                self._python_executable,
                "-m",
                "pytest",
                target.path,
                f"--junitxml={report_path}",
            ]

            try:
                completed = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=self._timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return self._execution_error(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    started=started,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    error_kind="timeout",
                    diagnostic="Pytest execution timed out",
                )
            except OSError as exc:
                return self._execution_error(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    started=started,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    error_kind="process_failure",
                    diagnostic=f"Pytest execution failed: {exc}",
                )

            try:
                report = self._parse_report(report_path)
            except (OSError, ET.ParseError, ValueError) as exc:
                kind = "missing_report" if not report_path.exists() else "invalid_report"
                return self._execution_error(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    started=started,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    error_kind=kind,
                    diagnostic=f"Pytest JUnit report unavailable or invalid: {exc}",
                    exit_code=completed.returncode,
                )

            inconsistency = self._protocol_inconsistency(
                exit_code=completed.returncode,
                report=report,
            )
            if inconsistency is not None:
                return self._execution_error(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    started=started,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    error_kind="inconsistent_result",
                    diagnostic=inconsistency,
                    exit_code=completed.returncode,
                    report=report,
                )

            if completed.returncode == 0:
                status = QualityStatus.PASS
                evidence_result = QualityEvidenceResult.PASS
                findings: tuple[QualityFinding, ...] = ()
            elif completed.returncode == 1:
                status = QualityStatus.FAIL
                evidence_result = QualityEvidenceResult.FAIL
                evidence_id = self._evidence_id_factory()
                evidence = self._evidence(
                    evidence_id=evidence_id,
                    rule=rule,
                    target=target,
                    result=evidence_result,
                    version=version,
                    metadata=self._report_metadata(completed.returncode, report),
                )
                findings = tuple(
                    self._finding(
                        failure=failure,
                        evidence_id=evidence_id,
                        rule=rule,
                        target=target,
                    )
                    for failure in report.failures
                )
                return QualityCheckResult(
                    check_id=check_id,
                    status=status,
                    findings=findings,
                    evidence=(evidence,),
                    duration_seconds=self._duration(started),
                    diagnostics=self._diagnostics(version_diagnostic),
                )
            else:
                return self._execution_error(
                    check_id=check_id,
                    rule=rule,
                    target=target,
                    started=started,
                    version=version,
                    version_diagnostic=version_diagnostic,
                    error_kind="pytest_error_exit",
                    diagnostic=(
                        "Pytest execution returned error exit status "
                        f"{completed.returncode}"
                    ),
                    exit_code=completed.returncode,
                    report=report,
                )

            evidence = self._evidence(
                evidence_id=self._evidence_id_factory(),
                rule=rule,
                target=target,
                result=evidence_result,
                version=version,
                metadata=self._report_metadata(completed.returncode, report),
            )
            return QualityCheckResult(
                check_id=check_id,
                status=status,
                findings=findings,
                evidence=(evidence,),
                duration_seconds=self._duration(started),
                diagnostics=self._diagnostics(version_diagnostic),
            )

    def _collect_version(self) -> tuple[str | None, str | None]:
        try:
            completed = subprocess.run(
                [self._python_executable, "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=self._timeout_seconds,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None, "Pytest version unavailable"

        if completed.returncode != 0:
            return None, "Pytest version unavailable"

        version = completed.stdout.strip()
        if not version:
            return None, "Pytest version unavailable"
        return version, None

    @staticmethod
    def _parse_report(report_path: Path) -> _PytestReport:
        if not report_path.is_file():
            raise OSError("JUnit XML report was not created")

        root = ET.parse(report_path).getroot()
        if root.tag not in {"testsuite", "testsuites"}:
            raise ValueError(f"unexpected JUnit root element {root.tag!r}")

        suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
        if not suites:
            raise ValueError("JUnit XML contains no testsuite")

        tests = 0
        failed = 0
        skipped = 0
        errors = 0
        duration = 0.0
        failures: list[_PytestCaseFailure] = []

        for suite in suites:
            tests += PytestQualityExecutor._int_attr(suite, "tests")
            failed += PytestQualityExecutor._int_attr(suite, "failures")
            skipped += PytestQualityExecutor._int_attr(suite, "skipped")
            errors += PytestQualityExecutor._int_attr(suite, "errors")
            duration += PytestQualityExecutor._float_attr(suite, "time")

            for case in suite.iter("testcase"):
                failure = case.find("failure")
                error = case.find("error")
                problem = failure if failure is not None else error
                if problem is None:
                    continue

                name = case.attrib.get("name", "").strip()
                classname = case.attrib.get("classname", "").strip()
                if not name:
                    raise ValueError("JUnit testcase failure is missing name")

                raw_message = (problem.attrib.get("message") or "").strip()
                body = (problem.text or "").strip()
                message = raw_message or body or f"{name} failed"

                location: str | None
                file_name = case.attrib.get("file", "").strip()
                line = case.attrib.get("line", "").strip()
                if file_name and line:
                    location = f"{file_name}:{line}"
                elif classname:
                    location = f"{classname}::{name}"
                else:
                    location = name

                failures.append(
                    _PytestCaseFailure(
                        name=name,
                        message=message,
                        location=location,
                    )
                )

        passed = tests - failed - skipped - errors
        if passed < 0:
            raise ValueError("JUnit XML contains inconsistent aggregate counts")
        if len(failures) != failed + errors:
            raise ValueError(
                "JUnit XML aggregate failures/errors do not match testcase details"
            )

        return _PytestReport(
            tests=tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            failures=tuple(failures),
        )

    @staticmethod
    def _int_attr(element: ET.Element, name: str) -> int:
        raw = element.attrib.get(name)
        if raw is None:
            if name in {"failures", "skipped", "errors"}:
                return 0
            raise ValueError(f"JUnit testsuite missing {name!r}")
        try:
            value = int(raw)
        except ValueError as exc:
            raise ValueError(f"JUnit {name!r} must be an integer") from exc
        if value < 0:
            raise ValueError(f"JUnit {name!r} must be non-negative")
        return value

    @staticmethod
    def _float_attr(element: ET.Element, name: str) -> float:
        raw = element.attrib.get(name, "0")
        try:
            value = float(raw)
        except ValueError as exc:
            raise ValueError(f"JUnit {name!r} must be numeric") from exc
        if value < 0:
            raise ValueError(f"JUnit {name!r} must be non-negative")
        return value

    @staticmethod
    def _protocol_inconsistency(
        *,
        exit_code: int,
        report: _PytestReport,
    ) -> str | None:
        problem_count = report.failed + report.errors

        if exit_code == 0 and problem_count:
            return "Pytest exit status 0 returned failed/error testcases"
        if exit_code == 1 and problem_count == 0:
            return "Pytest exit status 1 returned no failed/error testcases"
        return None

    def _finding(
        self,
        *,
        failure: _PytestCaseFailure,
        evidence_id: QualityEvidenceId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityFinding:
        return QualityFinding(
            id=self._finding_id_factory(),
            rule_id=rule.id,
            domain=rule.domain,
            severity=rule.severity,
            status=QualityStatus.FAIL,
            message=failure.message,
            target=target,
            location=failure.location,
            evidence_ids=(str(evidence_id),),
        )

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
            type=_TEST_EVIDENCE,
            source="quality.pytest",
            target=target,
            result=result,
            created_at=self._clock(),
            revision=None,
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            tool="pytest",
            tool_version=version,
            metadata=metadata,
            artifact=None,
        )

    @staticmethod
    def _report_metadata(
        exit_code: int,
        report: _PytestReport,
    ) -> tuple[tuple[str, str], ...]:
        return (
            ("exit_code", str(exit_code)),
            ("passed", str(report.passed)),
            ("failed", str(report.failed)),
            ("skipped", str(report.skipped)),
            ("errors", str(report.errors)),
            ("duration", PytestQualityExecutor._format_duration(report.duration)),
        )

    @staticmethod
    def _format_duration(value: float) -> str:
        return format(value, ".12g")

    def _execution_error(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
        started: float,
        version: str | None,
        version_diagnostic: str | None,
        error_kind: str,
        diagnostic: str,
        exit_code: int | None = None,
        report: _PytestReport | None = None,
    ) -> QualityCheckResult:
        metadata: tuple[tuple[str, str], ...]
        if report is not None and exit_code is not None:
            metadata = self._report_metadata(exit_code, report) + (
                ("error_kind", error_kind),
            )
        elif exit_code is not None:
            metadata = (
                ("exit_code", str(exit_code)),
                ("error_kind", error_kind),
            )
        else:
            metadata = (("error_kind", error_kind),)

        evidence = self._evidence(
            evidence_id=self._evidence_id_factory(),
            rule=rule,
            target=target,
            result=QualityEvidenceResult.ERROR,
            version=version,
            metadata=metadata,
        )
        return QualityCheckResult(
            check_id=check_id,
            status=QualityStatus.ERROR,
            findings=(),
            evidence=(evidence,),
            duration_seconds=self._duration(started),
            diagnostics=self._diagnostics(version_diagnostic, diagnostic),
        )

    @staticmethod
    def _diagnostics(*values: str | None) -> tuple[str, ...]:
        return tuple(value for value in values if value is not None)

    def _duration(self, started: float) -> float:
        return max(0.0, self._monotonic_clock() - started)
