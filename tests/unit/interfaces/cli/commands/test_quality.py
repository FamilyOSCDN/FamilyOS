"""Tests for the Phase 12 Quality check CLI adapter."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from typer.testing import CliRunner

from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.domain.quality import QualityCheckId, QualityStatus, QualityTarget
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


def _invoke(*extra: str):
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
    for option in (
        "--target-type",
        "--identifier",
        "--path",
        "--revision",
        "--version",
    ):
        assert option in result.stdout


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


def test_quality_check_does_not_expose_assess_or_report_yet() -> None:
    result = runner.invoke(app, ["quality", "--help"])

    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "assess" not in result.stdout
    assert "report" not in result.stdout
