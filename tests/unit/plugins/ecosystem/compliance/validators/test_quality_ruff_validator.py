"""Tests for the PLUGIN-QLT-001 (Ruff) validator."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

from familyos_cli.plugins.ecosystem.compliance.evidence_type import EvidenceType
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)
from familyos_cli.plugins.ecosystem.compliance.validators.quality_ruff_validator import (
    QualityRuffValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_source_is_clean(tmp_path: Path) -> None:
    """PASS when Ruff reports zero violations for the plugin subtree."""

    (tmp_path / "module.py").write_text(
        "def add(a: int, b: int) -> int:\n    return a + b\n",
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = QualityRuffValidator()

    run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.SUCCESS
    assert len(run_result.evidence) == 1

    evidence = run_result.evidence[0]
    assert evidence.type is EvidenceType.QUALITY
    assert evidence.source == str(tmp_path)
    assert evidence.trust_level.value == "local"
    assert evidence.producer == "quality.ruff"

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_ruff_violation_present(tmp_path: Path) -> None:
    """FAIL when Ruff reports a violation in the plugin subtree."""

    (tmp_path / "module.py").write_text("import os\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={})
    validator = QualityRuffValidator()

    run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.SUCCESS
    assert run_result.evidence[0].payload["violations"]

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_error_when_ruff_executable_missing(tmp_path: Path) -> None:
    """ERROR (not FAIL or PASS) when Ruff cannot be executed at all."""

    context = make_context(tmp_path, manifest={})
    validator = QualityRuffValidator()

    with patch(
        "familyos_cli.plugins.ecosystem.compliance.validators.quality_ruff_validator.subprocess.run",
        side_effect=FileNotFoundError("ruff not found"),
    ):
        run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.ERROR
    assert run_result.evidence == ()
    assert "ruff not found" in run_result.message.lower()


def test_error_when_ruff_reports_unexpected_exit_code(tmp_path: Path) -> None:
    """ERROR when Ruff exits with a status other than 0 or 1."""

    context = make_context(tmp_path, manifest={})
    validator = QualityRuffValidator()

    fake_process = subprocess.CompletedProcess(
        args=["ruff"],
        returncode=2,
        stdout="",
        stderr="invalid usage",
    )

    with patch(
        "familyos_cli.plugins.ecosystem.compliance.validators.quality_ruff_validator.subprocess.run",
        return_value=fake_process,
    ):
        run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.ERROR
    assert run_result.evidence == ()


def test_error_when_ruff_output_is_unparseable(tmp_path: Path) -> None:
    """ERROR when Ruff's stdout is not valid JSON."""

    context = make_context(tmp_path, manifest={})
    validator = QualityRuffValidator()

    fake_process = subprocess.CompletedProcess(
        args=["ruff"],
        returncode=1,
        stdout="not json",
        stderr="",
    )

    with patch(
        "familyos_cli.plugins.ecosystem.compliance.validators.quality_ruff_validator.subprocess.run",
        return_value=fake_process,
    ):
        run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.ERROR
    assert run_result.evidence == ()
