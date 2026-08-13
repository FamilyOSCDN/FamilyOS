"""End-to-end tests for the canonical CI validation CLI surface."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from familyos_cli.application.validation import (
    MANDATORY_CI_GATE_IDS,
    CiValidationResult,
    GateResult,
    ValidationStatus,
)
from familyos_cli.interfaces.cli.app import app
from familyos_cli.interfaces.cli.commands import validation

runner = CliRunner()


class _UseCase:
    def __init__(self, result: CiValidationResult) -> None:
        self.result = result

    def execute(self) -> CiValidationResult:
        return self.result


class _Context:
    def __init__(self, result: CiValidationResult) -> None:
        self.run_ci_validation = _UseCase(result)


def _result(
    failed_gate: str | None = None,
) -> CiValidationResult:
    return CiValidationResult(
        gates=tuple(
            GateResult(
                gate_id=gate_id,
                status=(
                    ValidationStatus.FAILED
                    if gate_id == failed_gate
                    else ValidationStatus.PASSED
                ),
                exit_code=1 if gate_id == failed_gate else 0,
            )
            for gate_id in MANDATORY_CI_GATE_IDS
        ),
    )


def _install_context(
    monkeypatch: pytest.MonkeyPatch,
    result: CiValidationResult,
) -> None:
    monkeypatch.setattr(validation, "CommandContext", lambda: _Context(result))


def test_ci_validation_succeeds_with_text_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_context(monkeypatch, _result())

    result = runner.invoke(app, ["validation", "ci"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "Canonical CI Validation: PASSED" in result.output
    for gate_id in MANDATORY_CI_GATE_IDS:
        assert f"- {gate_id}: PASSED" in result.output


def test_ci_validation_emits_deterministic_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    canonical_result = _result()
    _install_context(monkeypatch, canonical_result)

    first = runner.invoke(
        app,
        ["validation", "ci", "--format", "json"],
        catch_exceptions=False,
    )
    second = runner.invoke(
        app,
        ["validation", "ci", "--format", "json"],
        catch_exceptions=False,
    )

    assert first.exit_code == 0
    assert first.output == second.output
    payload = json.loads(first.output)
    assert [gate["id"] for gate in payload["gates"]] == list(
        MANDATORY_CI_GATE_IDS,
    )


def test_ci_validation_writes_json_output_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_context(monkeypatch, _result())
    output_path = tmp_path / "ci-validation.json"

    result = runner.invoke(
        app,
        ["validation", "ci", "--output", str(output_path)],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert json.loads(output_path.read_text(encoding="utf-8"))["status"] == "passed"


def test_failure_returns_nonzero_after_writing_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_context(monkeypatch, _result("mypy"))
    output_path = tmp_path / "ci-validation.json"

    result = runner.invoke(
        app,
        ["validation", "ci", "--output", str(output_path)],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert next(gate for gate in payload["gates"] if gate["id"] == "mypy")[
        "status"
    ] == "failed"
