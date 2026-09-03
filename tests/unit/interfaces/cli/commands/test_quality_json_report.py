"""CLI boundaries for the versioned structured Quality report."""

import json
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
import typer
from typer.testing import CliRunner, Result

from familyos_cli.application.quality import (
    QualityAssessmentExecutionResult,
    QualityCheckResult,
)
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.interfaces.cli.app import app
from familyos_cli.interfaces.cli.commands import quality as command

runner = CliRunner()


def output() -> QualityAssessmentExecutionResult:
    target = QualityTarget(target_type="documentation", identifier="returned-id", path="returned/path")
    assessment = QualityAssessment(
        id=QualityAssessmentId("QLT-ASMT-JSON"), target=target, revision=None,
        profile="QLT-PROFILE-DOCUMENTATION@1.0.0", status=QualityStatus.ERROR,
        quality_state=QualityAssessmentState.UNKNOWN, evidence_ids=(), finding_ids=(),
        created_at=datetime(2026, 9, 3, tzinfo=UTC),
    )
    check = QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-DOC"), status=QualityStatus.ERROR,
        diagnostics=("Impossible de lire le document.",),
    )
    return QualityAssessmentExecutionResult(assessment, (check,))


@dataclass
class Service:
    result: QualityAssessmentExecutionResult
    error: Exception | None = None
    calls: int = 0
    target: QualityTarget | None = None
    log: str | None = None

    def execute_with_results(self, target: QualityTarget) -> QualityAssessmentExecutionResult:
        self.calls += 1
        self.target = target
        if self.log:
            print(self.log)
        if self.error:
            raise self.error
        return self.result

    def execute(self, target: QualityTarget) -> QualityAssessment:
        raise AssertionError("JSON reporting must use the detailed execution")


def install(monkeypatch: pytest.MonkeyPatch) -> Service:
    service = Service(output())
    monkeypatch.setattr(command, "CommandContext", lambda: SimpleNamespace(quality_assessment=service))
    return service


def invoke(*options: str) -> Result:
    return runner.invoke(app, [
        "quality", "report", "--target-type", "repository", "--identifier", "input-id",
        "--path", ".", "--format", "json", *options,
    ])


def test_json_uses_one_detailed_execution_and_returned_canonical_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = install(monkeypatch)

    result = invoke("--revision", "input-revision", "--version", "input-version")

    assert result.exit_code == 2
    assert service.calls == 1
    assert service.target == QualityTarget(
        target_type="repository", identifier="input-id", path=".",
        revision="input-revision", version="input-version",
    )
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "1.0.0"
    assert payload["assessment"]["target"]["identifier"] == "returned-id"
    assert payload["assessment"]["target"]["path"] == "returned/path"
    assert payload["assessment"]["target"]["revision"] is None
    assert payload["check_results"][0]["diagnostics"] == ["Impossible de lire le document."]
    assert result.stderr == ""


@pytest.mark.parametrize(
    ("status", "exits"), [
        (QualityStatus.PASS, (0, 0, 1, 2)), (QualityStatus.WARNING, (0, 0, 1, 2)),
        (QualityStatus.FAIL, (0, 0, 1, 2)), (QualityStatus.SKIPPED, (0, 0, 1, 2)),
        (QualityStatus.ERROR, (2, 2, 2, 2)), (QualityStatus.UNKNOWN, (2, 2, 2, 2)),
    ],
)
@pytest.mark.parametrize(
    ("state", "index"), [
        (QualityAssessmentState.PASS, 0), (QualityAssessmentState.PASS_WITH_WARNINGS, 1),
        (QualityAssessmentState.FAIL, 2), (QualityAssessmentState.UNKNOWN, 3),
    ],
)
def test_json_uses_frozen_exit_policy_after_emitting_report(
    monkeypatch: pytest.MonkeyPatch, status: QualityStatus,
    exits: tuple[int, int, int, int], state: QualityAssessmentState, index: int,
) -> None:
    service = install(monkeypatch)
    service.result = replace(service.result, assessment=replace(service.result.assessment, status=status, quality_state=state))

    result = invoke()

    assert result.exit_code == exits[index]
    assert json.loads(result.stdout)["assessment"]["status"] == status.value
    assert json.loads(result.stdout)["assessment"]["quality_state"] == state.value
    assert result.stderr == ""


@pytest.mark.parametrize("options", [
    ("--format", "xml"), ("--format", "JSON"), ("--format", ""),
    ("--output", ""), ("--format", "text", "--output", "report.json"),
    ("--target-type", ""), ("--identifier", ""), ("--path", ""), ("--revision", ""),
])
def test_invalid_options_fail_before_execution(
    monkeypatch: pytest.MonkeyPatch, options: tuple[str, ...],
) -> None:
    service = install(monkeypatch)
    result = invoke(*options)
    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr
    assert service.calls == 0


@pytest.mark.parametrize("error", [ValueError("bad profile"), TypeError("bad result"), RuntimeError("executor defect"), OSError("read failure")])
def test_execution_failure_produces_only_stderr_and_preserves_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, error: Exception,
) -> None:
    service = install(monkeypatch)
    service.error = error
    destination = tmp_path / "report.json"
    destination.write_text("previous", encoding="utf-8")

    result = invoke("--output", str(destination))

    assert result.exit_code == 2
    assert str(error) in result.stderr
    assert result.stdout == ""
    assert destination.read_text() == "previous"
    assert service.calls == 1


def test_incidental_execution_stdout_is_retained_on_stderr(monkeypatch: pytest.MonkeyPatch) -> None:
    service = install(monkeypatch)
    service.log = "executor diagnostic"
    result = invoke()
    assert json.loads(result.stdout)["schema_version"] == "1.0.0"
    assert result.stderr == "executor diagnostic\n"


def test_file_destination_gets_complete_report_with_empty_stdout(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    service = install(monkeypatch)
    destination = tmp_path / "report.json"
    destination.write_text("previous", encoding="utf-8")
    result = invoke("--output", str(destination))
    assert result.exit_code == 2
    assert result.stdout == result.stderr == ""
    assert json.loads(destination.read_text())["assessment"]["id"] == str(service.result.assessment.id)
    assert service.calls == 1


def test_dash_destination_means_stdout(monkeypatch: pytest.MonkeyPatch) -> None:
    install(monkeypatch)
    result = invoke("--output", "-")
    assert result.exit_code == 2
    assert json.loads(result.stdout)["schema_version"] == "1.0.0"
    assert result.stderr == ""


def test_serialization_error_preserves_existing_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    service = install(monkeypatch)
    check = replace(service.result.check_results[0], duration_seconds=float("nan"))
    service.result = replace(service.result, check_results=(check,))
    destination = tmp_path / "report.json"
    destination.write_text("previous", encoding="utf-8")
    result = invoke("--output", str(destination))
    assert result.exit_code == 2
    assert result.stdout == ""
    assert "Out of range float" in result.stderr
    assert destination.read_text() == "previous"


def test_file_write_error_takes_precedence_over_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    service = install(monkeypatch)
    service.result = replace(service.result, assessment=replace(
        service.result.assessment, status=QualityStatus.PASS, quality_state=QualityAssessmentState.PASS,
    ))
    result = invoke("--output", str(tmp_path / "missing" / "report.json"))
    assert result.exit_code == 2
    assert result.stdout == ""
    assert "Quality JSON report failed:" in result.stderr


def test_stdout_write_failure_is_an_operational_error(monkeypatch: pytest.MonkeyPatch) -> None:
    install(monkeypatch)
    original_echo = typer.echo

    def echo(message: object, *, nl: bool = True, err: bool = False) -> None:
        if err:
            original_echo(message, nl=nl, err=True)
        else:
            raise OSError("stdout unavailable")

    monkeypatch.setattr(typer, "echo", echo)
    result = invoke()
    assert result.exit_code == 2
    assert result.stdout == ""
    assert result.stderr == "Quality JSON report failed: stdout unavailable\n"
