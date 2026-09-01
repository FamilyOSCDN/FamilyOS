from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pytest

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityFindingId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.quality import PytestQualityExecutor


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-PYTEST-001"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-QLT"),
        severity=QualitySeverity.HIGH,
        description="Pytest must pass",
        executor="pytest",
    )


def _target(path: str = "tests/unit") -> QualityTarget:
    return QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path=path,
    )


def _executor(
    *,
    monotonic_values: tuple[float, float] = (10.0, 10.25),
) -> PytestQualityExecutor:
    finding_counter = iter(range(1, 50))
    evidence_counter = iter(range(1, 50))
    return PytestQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-PYTEST-{next(finding_counter):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-PYTEST-{next(evidence_counter):03d}"
        ),
        clock=lambda: datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
        monotonic_clock=iter(monotonic_values).__next__,
        python_executable="/python",
    )


def _completed(
    *,
    returncode: int,
    stdout: str = "",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def _report_path(command: list[str]) -> Path:
    option = next(item for item in command if item.startswith("--junitxml="))
    return Path(option.split("=", 1)[1])


def _write_report(
    command: list[str],
    *,
    tests: int,
    failures: int = 0,
    errors: int = 0,
    skipped: int = 0,
    duration: str = "0.125",
    cases: str = "",
) -> None:
    _report_path(command).write_text(
        (
            '<?xml version="1.0" encoding="utf-8"?>'
            "<testsuites>"
            f'<testsuite name="pytest" errors="{errors}" failures="{failures}" '
            f'skipped="{skipped}" tests="{tests}" time="{duration}">'
            f"{cases}"
            "</testsuite>"
            "</testsuites>"
        ),
        encoding="utf-8",
    )


def _version_or_execution(
    command: list[str],
    *,
    returncode: int,
    report: dict[str, object],
) -> subprocess.CompletedProcess[str]:
    if command[-1] == "--version":
        return _completed(returncode=0, stdout="pytest 9.1.1\n")
    _write_report(command, **report)
    return _completed(returncode=returncode)


def test_pass_produces_test_evidence_and_canonical_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return _version_or_execution(
            command,
            returncode=0,
            report={"tests": 2},
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1
    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.type.value == "TEST"
    assert evidence.source == "quality.pytest"
    assert evidence.tool == "pytest"
    assert evidence.tool_version == "pytest 9.1.1"
    assert evidence.revision is None
    assert evidence.metadata == (
        ("exit_code", "0"),
        ("passed", "2"),
        ("failed", "0"),
        ("skipped", "0"),
        ("errors", "0"),
        ("duration", "0.125"),
    )
    assert result.duration_seconds == 0.25
    assert result.diagnostics == ()
    assert calls[0] == ["/python", "-m", "pytest", "--version"]
    assert calls[1][:5] == ["/python", "-m", "pytest", "tests/unit", calls[1][4]]
    assert calls[1][4].startswith("--junitxml=")


def test_exit_one_failure_maps_each_failed_test_to_governed_finding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cases = (
        '<testcase classname="tests.test_example" name="test_one" time="0.01">'
        '<failure message="assert 1 == 2">trace</failure>'
        "</testcase>"
        '<testcase classname="tests.test_example" name="test_two" time="0.02">'
        '<failure message="assert False">trace</failure>'
        "</testcase>"
    )

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return _version_or_execution(
            command,
            returncode=1,
            report={"tests": 2, "failures": 2, "cases": cases},
        )

    monkeypatch.setattr(subprocess, "run", run)

    rule = _rule()
    target = _target()
    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 2
    assert len(result.evidence) == 1

    first = result.findings[0]
    assert first.rule_id == rule.id
    assert first.domain == rule.domain
    assert first.severity == rule.severity
    assert first.status is QualityStatus.FAIL
    assert first.message == "assert 1 == 2"
    assert first.location == "tests.test_example::test_one"
    assert first.target is target
    assert first.evidence_ids == ("QLT-EVID-PYTEST-001",)

    assert result.evidence[0].result is QualityEvidenceResult.FAIL
    assert ("failed", "2") in result.evidence[0].metadata


def test_exit_one_setup_error_is_fail_and_becomes_finding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cases = (
        '<testcase classname="tests.test_fixture" name="test_needs_fixture">'
        '<error message="fixture setup failed">trace</error>'
        "</testcase>"
    )

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return _version_or_execution(
            command,
            returncode=1,
            report={"tests": 1, "errors": 1, "cases": cases},
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 1
    assert result.findings[0].message == "fixture setup failed"
    assert ("errors", "1") in result.evidence[0].metadata


def test_skipped_tests_are_preserved_without_causing_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cases = (
        '<testcase classname="tests.test_example" name="test_ok"/>'
        '<testcase classname="tests.test_example" name="test_skip">'
        '<skipped message="not supported"/>'
        "</testcase>"
    )

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return _version_or_execution(
            command,
            returncode=0,
            report={"tests": 2, "skipped": 1, "cases": cases},
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert ("passed", "1") in result.evidence[0].metadata
    assert ("skipped", "1") in result.evidence[0].metadata


@pytest.mark.parametrize("returncode", [2, 3, 4, 5, 6])
def test_pytest_error_exit_codes_are_quality_error_without_findings(
    monkeypatch: pytest.MonkeyPatch,
    returncode: int,
) -> None:
    cases = ""
    errors = 0
    tests = 0
    if returncode == 2:
        cases = (
            '<testcase classname="" name="collection">'
            '<error message="collection failure">trace</error>'
            "</testcase>"
        )
        errors = 1
        tests = 1

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return _version_or_execution(
            command,
            returncode=returncode,
            report={
                "tests": tests,
                "errors": errors,
                "cases": cases,
            },
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("exit_code", str(returncode)) in result.evidence[0].metadata
    assert ("error_kind", "pytest_error_exit") in result.evidence[0].metadata


def test_no_tests_collected_exit_five_is_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return _version_or_execution(
            command,
            returncode=5,
            report={"tests": 0},
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert ("exit_code", "5") in result.evidence[0].metadata


@pytest.mark.parametrize(
    ("returncode", "report", "expected"),
    [
        (
            0,
            {
                "tests": 1,
                "failures": 1,
                "cases": (
                    '<testcase name="test_bad">'
                    '<failure message="bad">trace</failure>'
                    "</testcase>"
                ),
            },
            "exit status 0 returned failed/error testcases",
        ),
        (
            1,
            {"tests": 1},
            "exit status 1 returned no failed/error testcases",
        ),
    ],
)
def test_exit_code_and_junit_inconsistency_is_error(
    monkeypatch: pytest.MonkeyPatch,
    returncode: int,
    report: dict[str, object],
    expected: str,
) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return _version_or_execution(
            command,
            returncode=returncode,
            report=report,
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert ("error_kind", "inconsistent_result") in result.evidence[0].metadata
    assert expected in result.diagnostics[-1]


def test_missing_junit_report_is_error_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="pytest 9.1.1\n")
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("error_kind", "missing_report") in result.evidence[0].metadata


def test_malformed_junit_report_is_error_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="pytest 9.1.1\n")
        _report_path(command).write_text("<testsuites>", encoding="utf-8")
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert ("error_kind", "invalid_report") in result.evidence[0].metadata


def test_timeout_is_error_with_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=0, stdout="pytest 9.1.1\n")
        raise subprocess.TimeoutExpired(command, timeout=120)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence[0].metadata == (("error_kind", "timeout"),)
    assert result.diagnostics == ("Pytest execution timed out",)


def test_os_failure_is_error_with_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=0, stdout="pytest 9.1.1\n")
        raise OSError("cannot execute")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence[0].metadata == (("error_kind", "process_failure"),)
    assert result.diagnostics == ("Pytest execution failed: cannot execute",)


def test_version_failure_is_non_fatal(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=2)
        _write_report(command, tests=1)
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.evidence[0].tool_version is None
    assert result.diagnostics == ("Pytest version unavailable",)


def test_missing_target_path_is_error_without_execution_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("subprocess must not run")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=QualityTarget("repository", "familyos-cli"),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert result.evidence == ()
    assert result.diagnostics == (
        "Pytest Quality target requires QualityTarget.path",
    )


def test_junit_aggregate_mismatch_is_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="pytest 9.1.1\n")
        _write_report(
            command,
            tests=1,
            failures=1,
            cases="",
        )
        return _completed(returncode=1)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert ("error_kind", "invalid_report") in result.evidence[0].metadata
