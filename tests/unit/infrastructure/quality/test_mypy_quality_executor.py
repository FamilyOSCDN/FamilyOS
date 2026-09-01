from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
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
from familyos_cli.infrastructure.quality import MypyQualityExecutor


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-MYPY-001"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-QLT"),
        severity=QualitySeverity.HIGH,
        description="MyPy must pass",
        executor="mypy",
    )


def _target(path: str = ".") -> QualityTarget:
    return QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path=path,
    )


def _executor(
    *,
    monotonic_values: tuple[float, float] = (10.0, 10.25),
) -> MypyQualityExecutor:
    finding_counter = iter(range(1, 40))
    evidence_counter = iter(range(1, 40))
    return MypyQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-MYPY-{next(finding_counter):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-MYPY-{next(evidence_counter):03d}"
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


def _mypy_diagnostic(
    *,
    code: str | None = "return-value",
    message: str = 'Incompatible return value type (got "str", expected "int")',
    column: int | None = 11,
) -> dict[str, Any]:
    return {
        "file": "src/example.py",
        "line": 2,
        "column": column,
        "end_line": 2,
        "end_column": 20,
        "message": message,
        "hint": None,
        "code": code,
        "severity": "error",
    }


def _json_lines(*records: dict[str, Any]) -> str:
    return "\n".join(json.dumps(record) for record in records) + "\n"


def _force_nonempty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        MypyQualityExecutor,
        "_is_existing_target_without_python_sources",
        staticmethod(lambda path: False),
    )


def test_pass_normalizes_execution_and_produces_type_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    _force_nonempty(monkeypatch)

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0 (compiled: yes)\n")
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.type.value == "TYPE_VERIFICATION"
    assert evidence.source == "quality.mypy"
    assert evidence.tool == "mypy"
    assert evidence.tool_version == "mypy 2.3.0 (compiled: yes)"
    assert evidence.revision is None
    assert evidence.metadata == (
        ("exit_code", "0"),
        ("diagnostic_count", "0"),
        ("mypy_codes", "[]"),
    )
    assert result.duration_seconds == 0.25
    assert result.diagnostics == ()
    assert calls == [
        ["/python", "-m", "mypy", "--version"],
        ["/python", "-m", "mypy", ".", "--output=json"],
    ]


def test_fail_maps_multiple_diagnostics_and_preserves_native_codes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _force_nonempty(monkeypatch)
    payload = _json_lines(
        _mypy_diagnostic(),
        _mypy_diagnostic(
            code="assignment",
            message="Incompatible types in assignment",
            column=4,
        ),
    )

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0 (compiled: yes)\n")
        return _completed(returncode=1, stdout=payload)

    monkeypatch.setattr(subprocess, "run", run)

    rule = _rule()
    target = _target()
    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 2

    first = result.findings[0]
    assert first.rule_id == rule.id
    assert first.domain == rule.domain
    assert first.severity == rule.severity
    assert first.status is QualityStatus.FAIL
    assert first.message.startswith("Incompatible return value type")
    assert first.location == "src/example.py:2:11"
    assert first.target is target
    assert first.evidence_ids == ("QLT-EVID-MYPY-001",)

    second = result.findings[1]
    assert second.location == "src/example.py:2:4"
    assert second.severity == rule.severity

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.FAIL
    assert evidence.metadata == (
        ("exit_code", "1"),
        ("diagnostic_count", "2"),
        ("mypy_codes", '["return-value","assignment"]'),
    )


def test_native_mypy_severity_does_not_override_governed_severity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _force_nonempty(monkeypatch)
    payload = _mypy_diagnostic()
    payload["severity"] = "note"

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        return _completed(returncode=1, stdout=_json_lines(payload))

    monkeypatch.setattr(subprocess, "run", run)

    rule = _rule()
    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=rule,
        target=_target(),
    )

    assert result.status is QualityStatus.FAIL
    assert result.findings[0].severity == rule.severity


def test_optional_column_and_code_are_supported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _force_nonempty(monkeypatch)

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        return _completed(
            returncode=1,
            stdout=_json_lines(_mypy_diagnostic(code=None, column=None)),
        )

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.FAIL
    assert result.findings[0].location == "src/example.py:2"
    assert result.evidence[0].metadata == (
        ("exit_code", "1"),
        ("diagnostic_count", "1"),
        ("mypy_codes", "[]"),
    )


@pytest.mark.parametrize(
    ("returncode", "stdout", "expected", "error_kind"),
    [
        (2, "", "unexpected exit status 2", "unexpected_exit"),
        (1, "not-json\n", "invalid JSON Lines", "invalid_json"),
        (1, '["not-object"]\n', "JSON object", "invalid_json"),
        (
            0,
            _json_lines(_mypy_diagnostic()),
            "exit status 0 returned type-checking findings",
            "inconsistent_result",
        ),
        (
            1,
            "",
            "exit status 1 returned no type-checking findings",
            "inconsistent_result",
        ),
    ],
)
def test_execution_protocol_errors_produce_error_evidence(
    monkeypatch: pytest.MonkeyPatch,
    returncode: int,
    stdout: str,
    expected: str,
    error_kind: str,
) -> None:
    _force_nonempty(monkeypatch)

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        return _completed(returncode=returncode, stdout=stdout)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("error_kind", error_kind) in result.evidence[0].metadata
    assert any(expected in diagnostic for diagnostic in result.diagnostics)


@pytest.mark.parametrize(
    "payload",
    [
        {"line": 2, "column": 1, "message": "x", "code": "x"},
        {"file": "x.py", "line": "2", "column": 1, "message": "x", "code": "x"},
        {"file": "x.py", "line": 2, "column": "1", "message": "x", "code": "x"},
        {"file": "x.py", "line": 2, "column": 1, "message": "", "code": "x"},
        {"file": "x.py", "line": 2, "column": 1, "message": "x", "code": ""},
    ],
)
def test_invalid_diagnostic_payload_is_error_with_evidence(
    monkeypatch: pytest.MonkeyPatch,
    payload: dict[str, Any],
) -> None:
    _force_nonempty(monkeypatch)

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        return _completed(returncode=1, stdout=_json_lines(payload))

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.findings == ()
    assert len(result.evidence) == 1
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert ("error_kind", "invalid_diagnostic") in result.evidence[0].metadata
    assert "invalid" in result.diagnostics[-1]


def test_timeout_is_error_with_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    _force_nonempty(monkeypatch)
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        raise subprocess.TimeoutExpired(command, timeout=120)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert result.evidence[0].metadata == (("error_kind", "timeout"),)
    assert result.diagnostics == ("MyPy execution timed out",)


def test_os_failure_is_error_with_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    _force_nonempty(monkeypatch)
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        raise OSError("cannot execute")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.evidence[0].result is QualityEvidenceResult.ERROR
    assert result.evidence[0].metadata == (("error_kind", "process_failure"),)
    assert result.diagnostics == ("MyPy execution failed: cannot execute",)


def test_version_failure_is_non_fatal(monkeypatch: pytest.MonkeyPatch) -> None:
    _force_nonempty(monkeypatch)
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=2)
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.PASS
    assert result.evidence[0].tool_version is None
    assert result.diagnostics == ("MyPy version unavailable",)


def test_version_failure_diagnostic_survives_execution_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _force_nonempty(monkeypatch)
    calls = 0

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return _completed(returncode=2)
        return _completed(returncode=2, stderr="tool failed")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(),
    )

    assert result.status is QualityStatus.ERROR
    assert result.evidence[0].tool_version is None
    assert result.diagnostics[0] == "MyPy version unavailable"
    assert "unexpected exit status 2" in result.diagnostics[1]


def test_missing_target_path_is_error_without_execution_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("subprocess must not run")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=QualityTarget("repository", "familyos-cli"),
    )

    assert result.status is QualityStatus.ERROR
    assert result.evidence == ()
    assert result.diagnostics == (
        "MyPy Quality target requires QualityTarget.path",
    )


def test_empty_directory_is_compatibility_pass_without_subprocess(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").write_text("nothing to type-check\n", encoding="utf-8")

    def run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("subprocess must not run for empty Python target")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(str(tmp_path)),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.type.value == "TYPE_VERIFICATION"
    assert evidence.source == "quality.mypy"
    assert evidence.tool == "mypy"
    assert evidence.tool_version is None
    assert evidence.metadata == (
        ("diagnostic_count", "0"),
        ("mypy_codes", "[]"),
        ("execution", "not_run_no_python_sources"),
    )
    assert result.diagnostics == (
        "No Python source files found; nothing to type-check.",
    )


def test_directory_with_pyi_source_is_not_treated_as_empty(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "example.pyi").write_text("x: int\n", encoding="utf-8")
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        return _completed(returncode=0)

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(str(tmp_path)),
    )

    assert result.status is QualityStatus.PASS
    assert calls == [
        ["/python", "-m", "mypy", "--version"],
        ["/python", "-m", "mypy", str(tmp_path), "--output=json"],
    ]


def test_nonexistent_target_is_delegated_to_mypy_and_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing"
    calls: list[list[str]] = []

    def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[-1] == "--version":
            return _completed(returncode=0, stdout="mypy 2.3.0\n")
        return _completed(returncode=2, stderr="can't read file")

    monkeypatch.setattr(subprocess, "run", run)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY"),
        rule=_rule(),
        target=_target(str(missing)),
    )

    assert result.status is QualityStatus.ERROR
    assert len(calls) == 2
    assert ("error_kind", "unexpected_exit") in result.evidence[0].metadata
