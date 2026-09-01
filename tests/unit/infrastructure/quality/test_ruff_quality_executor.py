from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from typing import Any

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
from familyos_cli.infrastructure.quality import RuffQualityExecutor


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-RUFF-001"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-QLT"),
        severity=QualitySeverity.MEDIUM,
        description="Ruff must pass",
        executor="ruff",
    )


def _target() -> QualityTarget:
    return QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path=".",
    )


def _executor() -> RuffQualityExecutor:
    finding_counter = iter(range(1, 20))
    evidence_counter = iter(range(1, 20))
    return RuffQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-RUFF-{next(finding_counter):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-RUFF-{next(evidence_counter):03d}"
        ),
        clock=lambda: datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
        monotonic_clock=iter((10.0, 10.25)).__next__,
        python_executable="/python",
    )


def _completed(
    *,
    returncode: int,
    stdout: str = "[]",
    stderr: str = "",
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def _ruff_violation(
    *,
    code: str = "F401",
    message: str = "os imported but unused",
) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "filename": "src/example.py",
        "location": {"row": 3, "column": 1},
        "end_location": {"row": 3, "column": 10},
        "fix": None,
        "noqa_row": 3,
        "url": "https://docs.astral.sh/ruff/rules/unused-import/",
    }


def test_pass_normalizes_execution_and_produces_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="ruff 0.15.21\n")
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.PASS
    assert result.evidence[0].type.value == "STATIC_ANALYSIS"
    assert result.evidence[0].tool == "ruff"
    assert result.evidence[0].tool_version == "ruff 0.15.21"
    assert result.evidence[0].revision is None
    assert result.evidence[0].metadata == (
        ("exit_code", "0"),
        ("violation_count", "0"),
        ("ruff_codes", "[]"),
    )
    assert result.duration_seconds == 0.25
    assert result.diagnostics == ()
    assert calls == [
        ["/python", "-m", "ruff", "--version"],
        ["/python", "-m", "ruff", "check", ".", "--output-format=json"],
    ]


def test_fail_maps_violation_and_preserves_native_ruff_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = json.dumps([_ruff_violation()])

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="ruff 0.15.21\n")
        return _completed(returncode=1, stdout=payload)

    monkeypatch.setattr(subprocess, "run", run)

    rule = _rule()
    target = _target()
    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 1
    finding = result.findings[0]
    assert finding.rule_id == rule.id
    assert finding.domain == rule.domain
    assert finding.severity == rule.severity
    assert finding.status is QualityStatus.FAIL
    assert finding.message == "os imported but unused"
    assert finding.location == "src/example.py:3:1"
    assert finding.target is target
    assert finding.evidence_ids == ("QLT-EVID-RUFF-001",)

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.FAIL
    assert evidence.metadata == (
        ("exit_code", "1"),
        ("violation_count", "1"),
        ("ruff_codes", '["F401"]'),
    )


@pytest.mark.parametrize(
    ("returncode", "stdout", "expected", "error_kind"),
    [
        (2, "", "unexpected exit status 2", "unexpected_exit"),
        (0, "not-json", "invalid JSON", "invalid_json"),
        (0, "{}", "must be a list", "invalid_json_shape"),
        (0, '[{"message":"x"}]', "exit status 0 returned violations", "inconsistent_result"),
        (1, "[]", "exit status 1 returned no violations", "inconsistent_result"),
    ],
)
def test_execution_protocol_errors_produce_error_evidence(
    monkeypatch: pytest.MonkeyPatch,
    returncode: int,
    stdout: str,
    expected: str,
    error_kind: str,
) -> None:
    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="ruff 0.15.21\n")
        return _completed(returncode=returncode, stdout=stdout)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("error_kind", error_kind) in result.evidence[0].metadata
    assert any(expected in diagnostic for diagnostic in result.diagnostics)


def test_timeout_is_error_with_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return _completed(returncode=0, stdout="ruff 0.15.21\n")
        raise subprocess.TimeoutExpired(command, timeout=120)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert result.evidence[0].metadata == (("error_kind", "timeout"),)
    assert result.diagnostics == ("Ruff execution timed out",)


def test_os_failure_is_error_with_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return _completed(returncode=0, stdout="ruff 0.15.21\n")
        raise OSError("cannot execute")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert result.evidence[0].metadata == (("error_kind", "process_failure"),)
    assert result.diagnostics == ("Ruff execution failed: cannot execute",)


def test_version_failure_is_non_fatal(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=2, stderr="version failed")
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.evidence[0].tool_version is None
    assert result.diagnostics == ("Ruff version unavailable",)


def test_version_failure_diagnostic_survives_execution_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=2)
        return _completed(returncode=2, stderr="tool failed")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.evidence[0].tool_version is None
    assert result.diagnostics[0] == "Ruff version unavailable"
    assert "unexpected exit status 2" in result.diagnostics[1]


def test_missing_target_path_is_error_without_execution_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("subprocess must not run")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=QualityTarget("repository", "familyos-cli"),
    )

    assert result.status is QualityStatus.ERROR
    assert result.evidence == ()
    assert result.diagnostics == (
        "Ruff Quality target requires QualityTarget.path",
    )


def test_invalid_violation_payload_is_error_with_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = json.dumps([{"code": "F401", "message": "missing fields"}])

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="ruff 0.15.21\n")
        return _completed(returncode=1, stdout=payload)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-RUFF"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("error_kind", "invalid_violation") in result.evidence[0].metadata
    assert "invalid" in result.diagnostics[-1]
