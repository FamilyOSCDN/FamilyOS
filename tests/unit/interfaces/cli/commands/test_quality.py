"""Tests for the Phase 12 Quality CLI adapters."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime

import pytest
from click import unstyle
from typer.testing import CliRunner, Result

from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityEvidenceId,
    QualityFindingId,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.interfaces.cli.app import app
from familyos_cli.interfaces.cli.commands import quality as quality_command

runner = CliRunner()


def _result(check_id: str, status: QualityStatus) -> QualityCheckResult:
    return QualityCheckResult(
        check_id=QualityCheckId(check_id),
        status=status,
        findings=(),
        evidence=(),
        duration_seconds=0.0,
        diagnostics=(),
    )


@dataclass
class _ExecutionService:
    results: tuple[QualityCheckResult, ...] = ()
    error: Exception | None = None
    target: QualityTarget | None = None

    def execute(self, target: QualityTarget) -> tuple[QualityCheckResult, ...]:
        self.target = target
        if self.error is not None:
            raise self.error
        return self.results


class _CommandContext:
    service: _ExecutionService

    def __init__(self) -> None:
        self.quality_execution = self.service


def _install(
    monkeypatch: pytest.MonkeyPatch,
    *,
    results: tuple[QualityCheckResult, ...] = (),
    error: Exception | None = None,
) -> _ExecutionService:
    service = _ExecutionService(results=results, error=error)
    _CommandContext.service = service
    monkeypatch.setattr(quality_command, "CommandContext", _CommandContext)
    return service


def _invoke(*extra: str) -> Result:
    return runner.invoke(
        app,
        [
            "quality",
            "check",
            "--target-type",
            "repository",
            "--identifier",
            "familyos-cli",
            "--path",
            ".",
            *extra,
        ],
    )


def test_root_help_registers_quality_command_group() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "quality" in result.stdout
    assert "Quality Framework commands." in result.stdout


def test_quality_check_help_exposes_explicit_target_options() -> None:
    result = runner.invoke(app, ["quality", "check", "--help"])

    assert result.exit_code == 0
    output = unstyle(result.stdout)
    for option in (
        "--target-type",
        "--identifier",
        "--path",
        "--revision",
        "--version",
    ):
        assert option in output


def test_quality_check_constructs_canonical_target_and_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _install(
        monkeypatch,
        results=(_result("QLT-CHECK-RUFF", QualityStatus.PASS),),
    )

    result = _invoke("--revision", "abc123", "--version", "1.2.3")

    assert result.exit_code == 0
    assert service.target == QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path=".",
        revision="abc123",
        version="1.2.3",
    )


def test_quality_check_preserves_result_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install(
        monkeypatch,
        results=(
            _result("QLT-CHECK-MYPY", QualityStatus.PASS),
            _result("QLT-CHECK-RUFF", QualityStatus.WARNING),
        ),
    )

    result = _invoke()

    assert result.exit_code == 0
    assert result.stdout.index("QLT-CHECK-MYPY") < result.stdout.index("QLT-CHECK-RUFF")


@pytest.mark.parametrize(
    ("statuses", "expected_exit"),
    [
        ((QualityStatus.PASS,), 0),
        ((QualityStatus.PASS, QualityStatus.WARNING), 0),
        ((QualityStatus.FAIL,), 1),
        ((QualityStatus.UNKNOWN,), 2),
        ((QualityStatus.SKIPPED,), 2),
        ((QualityStatus.ERROR,), 2),
        ((QualityStatus.FAIL, QualityStatus.ERROR), 2),
    ],
)
def test_quality_check_uses_frozen_exit_policy(
    monkeypatch: pytest.MonkeyPatch,
    statuses: tuple[QualityStatus, ...],
    expected_exit: int,
) -> None:
    results = tuple(
        _result(f"QLT-CHECK-{index}", status)
        for index, status in enumerate(statuses, start=1)
    )
    _install(monkeypatch, results=results)

    result = _invoke()

    assert result.exit_code == expected_exit


def test_quality_check_empty_results_are_unreliable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install(monkeypatch)

    result = _invoke()

    assert result.exit_code == 2


@pytest.mark.parametrize(
    "error",
    [
        ValueError("profile resolution failed"),
        TypeError("invalid target"),
    ],
)
def test_quality_check_adapts_expected_execution_failures_to_exit_two(
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    _install(monkeypatch, error=error)

    result = _invoke()

    assert result.exit_code == 2
    assert str(error) in result.stderr


@dataclass
class _AssessmentService:
    assessment: QualityAssessment | None = None
    error: Exception | None = None
    target: QualityTarget | None = None
    calls: int = 0

    def execute(self, target: QualityTarget) -> QualityAssessment:
        self.calls += 1
        self.target = target
        if self.error is not None:
            raise self.error
        if self.assessment is None:
            raise AssertionError("assessment test double is not configured")
        return self.assessment


class _AssessmentCommandContext:
    service: _AssessmentService

    def __init__(self) -> None:
        self.quality_assessment = self.service


def _assessment(
    status: QualityStatus,
    state: QualityAssessmentState,
) -> QualityAssessment:
    target = QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path=".",
        revision="abc123",
    )
    return QualityAssessment(
        id=QualityAssessmentId("QLT-ASMT-CLI-TEST"),
        target=target,
        revision=target.revision,
        profile="QLT-PROFILE-REPOSITORY@1",
        status=status,
        quality_state=state,
        evidence_ids=(),
        finding_ids=(),
        created_at=datetime(2026, 9, 3, 10, 0, tzinfo=UTC),
    )


def _install_assessment(
    monkeypatch: pytest.MonkeyPatch,
    *,
    assessment: QualityAssessment | None = None,
    error: Exception | None = None,
) -> _AssessmentService:
    service = _AssessmentService(assessment=assessment, error=error)
    _AssessmentCommandContext.service = service
    monkeypatch.setattr(
        quality_command,
        "CommandContext",
        _AssessmentCommandContext,
    )
    return service


def _invoke_assess(*extra: str) -> Result:
    return runner.invoke(
        app,
        [
            "quality",
            "assess",
            "--target-type",
            "repository",
            "--identifier",
            "familyos-cli",
            "--path",
            ".",
            *extra,
        ],
    )


def test_quality_assess_help_exposes_explicit_target_options() -> None:
    result = runner.invoke(app, ["quality", "assess", "--help"])
    assert result.exit_code == 0
    output = unstyle(result.stdout)
    for option in (
        "--target-type",
        "--identifier",
        "--path",
        "--revision",
        "--version",
    ):
        assert option in output


def test_quality_assess_constructs_target_and_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = _install_assessment(
        monkeypatch,
        assessment=_assessment(
            QualityStatus.PASS,
            QualityAssessmentState.PASS,
        ),
    )
    result = _invoke_assess("--revision", "abc123", "--version", "1.2.3")
    assert result.exit_code == 0
    assert service.target == QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path=".",
        revision="abc123",
        version="1.2.3",
    )


@pytest.mark.parametrize(
    ("status", "state", "expected_exit"),
    [
        (QualityStatus.PASS, QualityAssessmentState.PASS, 0),
        (QualityStatus.WARNING, QualityAssessmentState.PASS_WITH_WARNINGS, 0),
        (QualityStatus.FAIL, QualityAssessmentState.FAIL, 1),
        (QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN, 2),
        (QualityStatus.ERROR, QualityAssessmentState.FAIL, 2),
        (QualityStatus.UNKNOWN, QualityAssessmentState.PASS, 2),
    ],
)
def test_quality_assess_uses_frozen_exit_policy(
    monkeypatch: pytest.MonkeyPatch,
    status: QualityStatus,
    state: QualityAssessmentState,
    expected_exit: int,
) -> None:
    _install_assessment(
        monkeypatch,
        assessment=_assessment(status, state),
    )
    result = _invoke_assess()
    assert result.exit_code == expected_exit


def test_quality_assess_renders_canonical_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_assessment(
        monkeypatch,
        assessment=_assessment(
            QualityStatus.PASS,
            QualityAssessmentState.PASS,
        ),
    )
    result = _invoke_assess("--revision", "abc123")
    assert result.exit_code == 0
    for expected in (
        "QLT-ASMT-CLI-TEST",
        "repository:familyos-cli",
        "QLT-PROFILE-REPOSITORY@1",
        "Status: PASS",
        "Quality State: PASS",
        "Revision: abc123",
        "Created At:",
    ):
        assert expected in result.stdout
    assert "Quality Gate" not in result.stdout
    assert "Risk" not in result.stdout


@pytest.mark.parametrize(
    "error",
    [
        ValueError("profile resolution failed"),
        TypeError("invalid target"),
    ],
)
def test_quality_assess_adapts_expected_failures_to_exit_two(
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    _install_assessment(monkeypatch, error=error)
    result = _invoke_assess()
    assert result.exit_code == 2
    assert str(error) in result.stderr


def test_quality_group_exposes_check_assess_and_report() -> None:
    result = runner.invoke(app, ["quality", "--help"])
    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "assess" in result.stdout
    assert "report" in result.stdout


def _invoke_report(*extra: str) -> Result:
    return runner.invoke(
        app,
        [
            "quality",
            "report",
            "--target-type",
            "repository",
            "--identifier",
            "familyos-cli",
            "--path",
            ".",
            *extra,
        ],
    )


def test_quality_report_help_exposes_only_authorized_options() -> None:
    result = runner.invoke(app, ["quality", "report", "--help"])

    assert result.exit_code == 0
    output = unstyle(result.stdout)
    for option in (
        "--target-type",
        "--identifier",
        "--path",
        "--revision",
        "--version",
        "--format",
        "--output",
    ):
        assert option in output
    assert "--json" not in output


@pytest.mark.parametrize("revision", [None, "abc123"])
@pytest.mark.parametrize("version", [None, "1.2.3"])
def test_quality_report_constructs_target_and_delegates_once(
    monkeypatch: pytest.MonkeyPatch,
    revision: str | None,
    version: str | None,
) -> None:
    service = _install_assessment(
        monkeypatch,
        assessment=_assessment(QualityStatus.PASS, QualityAssessmentState.PASS),
    )
    options = ["--path", "relative/repository"]
    if revision is not None:
        options.extend(("--revision", revision))
    if version is not None:
        options.extend(("--version", version))

    result = _invoke_report(*options)

    assert result.exit_code == 0
    assert service.calls == 1
    assert service.target == QualityTarget(
        target_type="repository",
        identifier="familyos-cli",
        path="relative/repository",
        revision=revision,
        version=version,
    )


def test_quality_report_renders_canonical_values_in_deterministic_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = QualityTarget(
        target_type="plugin",
        identifier="family.calendar",
        path="plugins/family.calendar",
        revision="returned-revision",
        version="4.5.6",
    )
    assessment = replace(
        _assessment(QualityStatus.WARNING, QualityAssessmentState.PASS_WITH_WARNINGS),
        target=target,
        revision=target.revision,
        evidence_ids=(
            QualityEvidenceId("QLT-EVID-Z"),
            QualityEvidenceId("QLT-EVID-A"),
            QualityEvidenceId("QLT-EVID-Z"),
        ),
        finding_ids=(
            QualityFindingId("QLT-FIND-Z"),
            QualityFindingId("QLT-FIND-A"),
        ),
    )
    _install_assessment(monkeypatch, assessment=assessment)

    first = _invoke_report("--revision", "input-revision", "--version", "1.2.3")
    second = _invoke_report("--revision", "input-revision", "--version", "1.2.3")

    assert first.exit_code == second.exit_code == 0
    assert first.stdout == second.stdout == (
        "Assessment ID: QLT-ASMT-CLI-TEST\n"
        "Target: plugin:family.calendar\n"
        "Path: plugins/family.calendar\n"
        "Revision: returned-revision\n"
        "Version: 4.5.6\n"
        "Profile: QLT-PROFILE-REPOSITORY@1\n"
        "Status: WARNING\n"
        "Quality State: PASS_WITH_WARNINGS\n"
        "Evidence IDs: QLT-EVID-Z, QLT-EVID-A, QLT-EVID-Z\n"
        "Finding IDs: QLT-FIND-Z, QLT-FIND-A\n"
        "Created At: 2026-09-03T10:00:00+00:00\n"
    )
    assert first.stderr == second.stderr == ""


@pytest.mark.parametrize(
    ("revision", "version", "expected_lines"),
    [
        (None, None, []),
        ("abc123", None, ["Revision: abc123"]),
        (None, "1.2.3", ["Version: 1.2.3"]),
        ("abc123", "1.2.3", ["Revision: abc123", "Version: 1.2.3"]),
    ],
)
def test_quality_report_renders_optional_target_values_when_present(
    monkeypatch: pytest.MonkeyPatch,
    revision: str | None,
    version: str | None,
    expected_lines: list[str],
) -> None:
    assessment = _assessment(QualityStatus.PASS, QualityAssessmentState.PASS)
    target = replace(assessment.target, revision=revision, version=version)
    _install_assessment(
        monkeypatch,
        assessment=replace(assessment, target=target, revision=revision),
    )

    result = _invoke_report()

    assert result.exit_code == 0
    assert [
        line
        for line in result.stdout.splitlines()
        if line.startswith(("Revision:", "Version:"))
    ] == expected_lines
    assert "Evidence IDs: -\n" in result.stdout
    assert "Finding IDs: -\n" in result.stdout


@pytest.mark.parametrize(
    ("status", "expected_exits"),
    [
        (QualityStatus.PASS, (0, 0, 1, 2)),
        (QualityStatus.WARNING, (0, 0, 1, 2)),
        (QualityStatus.FAIL, (0, 0, 1, 2)),
        (QualityStatus.SKIPPED, (0, 0, 1, 2)),
        (QualityStatus.ERROR, (2, 2, 2, 2)),
        (QualityStatus.UNKNOWN, (2, 2, 2, 2)),
    ],
)
@pytest.mark.parametrize(
    ("state", "state_index"),
    [
        (QualityAssessmentState.PASS, 0),
        (QualityAssessmentState.PASS_WITH_WARNINGS, 1),
        (QualityAssessmentState.FAIL, 2),
        (QualityAssessmentState.UNKNOWN, 3),
    ],
)
def test_quality_report_preserves_canonical_status_and_frozen_exit_policy(
    monkeypatch: pytest.MonkeyPatch,
    status: QualityStatus,
    expected_exits: tuple[int, int, int, int],
    state: QualityAssessmentState,
    state_index: int,
) -> None:
    _install_assessment(monkeypatch, assessment=_assessment(status, state))

    result = _invoke_report()

    assert result.exit_code == expected_exits[state_index]
    assert f"Status: {status.value}\n" in result.stdout
    assert f"Quality State: {state.value}\n" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize(
    "error",
    [TypeError("invalid assessment target"), ValueError("profile resolution failed")],
)
def test_quality_report_adapts_expected_execution_failures_to_exit_two(
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    service = _install_assessment(monkeypatch, error=error)

    result = _invoke_report()

    assert result.exit_code == 2
    assert str(error) in result.stderr
    assert result.stdout == ""
    assert service.calls == 1


@pytest.mark.parametrize(
    "option", ["--target-type", "--identifier", "--path", "--revision", "--version"]
)
def test_quality_report_rejects_invalid_target_before_execution(
    monkeypatch: pytest.MonkeyPatch,
    option: str,
) -> None:
    service = _install_assessment(monkeypatch)

    result = _invoke_report(option, "")

    assert result.exit_code == 2
    assert "must be non-empty" in result.stderr
    assert result.stdout == ""
    assert service.calls == 0


@pytest.mark.parametrize("missing_option", ["--target-type", "--identifier", "--path"])
def test_quality_report_requires_explicit_target_options(
    monkeypatch: pytest.MonkeyPatch,
    missing_option: str,
) -> None:
    service = _install_assessment(monkeypatch)
    options = {
        "--target-type": "repository",
        "--identifier": "familyos-cli",
        "--path": ".",
    }
    arguments = [
        argument
        for option, value in options.items()
        if option != missing_option
        for argument in (option, value)
    ]

    result = runner.invoke(app, ["quality", "report", *arguments])

    assert result.exit_code == 2
    assert missing_option in unstyle(result.stderr)
    assert service.calls == 0


@pytest.mark.parametrize("options", [("--json",)])
def test_quality_report_rejects_unadvertised_json_alias(
    monkeypatch: pytest.MonkeyPatch,
    options: tuple[str, ...],
) -> None:
    service = _install_assessment(monkeypatch)

    result = _invoke_report(*options)

    assert result.exit_code == 2
    assert "No such option" in result.stderr
    assert service.calls == 0


def test_quality_report_preserves_unexpected_execution_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error = RuntimeError("unexpected application defect")
    _install_assessment(monkeypatch, error=error)

    result = _invoke_report()

    assert result.exception is error
    assert result.stdout == ""
    assert result.stderr == ""


def test_quality_report_explicit_text_preserves_default_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_assessment(
        monkeypatch, assessment=_assessment(QualityStatus.PASS, QualityAssessmentState.PASS),
    )
    default = _invoke_report()
    explicit = _invoke_report("--format", "text")
    assert explicit.exit_code == default.exit_code == 0
    assert explicit.stdout == default.stdout
    assert explicit.stderr == default.stderr == ""


@pytest.mark.parametrize(
    "error",
    [
        TypeError("invalid report field"),
        ValueError("invalid report format"),
        RuntimeError("renderer failed"),
        OSError("report output unavailable"),
        UnicodeError("report encoding failed"),
    ],
)
def test_quality_report_rendering_failure_takes_precedence_over_quality_fail(
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    assessment = _assessment(QualityStatus.FAIL, QualityAssessmentState.FAIL)
    _install_assessment(monkeypatch, assessment=assessment)

    def fail_to_render(value: QualityAssessment) -> None:
        assert value is assessment
        raise error

    monkeypatch.setattr(quality_command, "_render_report", fail_to_render)

    result = _invoke_report()

    assert result.exit_code == 2
    assert f"Quality report rendering failed: {error}" in result.stderr
    assert result.stdout == ""
