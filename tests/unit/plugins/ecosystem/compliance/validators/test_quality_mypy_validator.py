"""Tests for the PLUGIN-QLT-002 (MyPy) validator."""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

from familyos_cli.plugins.ecosystem.compliance.evidence_type import EvidenceType
from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validator_status import (
    ValidatorStatus,
)
from familyos_cli.plugins.ecosystem.compliance.validators.quality_mypy_validator import (
    QualityMypyValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_pass_when_source_is_clean(tmp_path: Path) -> None:
    """PASS when MyPy reports zero type errors for the plugin subtree."""

    (tmp_path / "module.py").write_text(
        "def add(a: int, b: int) -> int:\n    return a + b\n",
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = QualityMypyValidator()

    run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.SUCCESS
    assert len(run_result.evidence) == 1

    evidence = run_result.evidence[0]
    assert evidence.type is EvidenceType.QUALITY
    assert evidence.source == str(tmp_path)
    assert evidence.trust_level.value == "local"
    assert evidence.producer == "quality.mypy"

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_pass_when_no_python_files_present(tmp_path: Path) -> None:
    """PASS (not ERROR) when the plugin subtree has no .py files.

    MyPy itself exits with a fatal usage error (status 2) when given a
    directory with no Python files, which would otherwise be
    indistinguishable from a genuine tool infrastructure failure.
    """

    (tmp_path / "plugin.yaml").write_text("id: acme.empty\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={})
    validator = QualityMypyValidator()

    run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.SUCCESS
    assert run_result.evidence[0].payload["errors"] == []

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_type_error_present(tmp_path: Path) -> None:
    """FAIL when MyPy reports a type error in the plugin subtree."""

    (tmp_path / "module.py").write_text(
        'def foo() -> int:\n    return "bad"\n',
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = QualityMypyValidator()

    run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.SUCCESS
    assert run_result.evidence[0].payload["errors"]

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL


def test_error_when_mypy_executable_missing(tmp_path: Path) -> None:
    """ERROR (not FAIL or PASS) when MyPy cannot be executed at all."""

    (tmp_path / "module.py").write_text("x: int = 1\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={})
    validator = QualityMypyValidator()

    with patch(
        "familyos_cli.plugins.ecosystem.compliance.validators.quality_mypy_validator.subprocess.run",
        side_effect=FileNotFoundError("mypy not found"),
    ):
        run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.ERROR
    assert run_result.evidence == ()
    assert "mypy not found" in run_result.message.lower()


def test_error_when_mypy_reports_unexpected_exit_code(tmp_path: Path) -> None:
    """ERROR when MyPy exits with a status other than 0 or 1."""

    (tmp_path / "module.py").write_text("x: int = 1\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={})
    validator = QualityMypyValidator()

    fake_process = subprocess.CompletedProcess(
        args=["mypy"],
        returncode=2,
        stdout="",
        stderr="fatal error",
    )

    with patch(
        "familyos_cli.plugins.ecosystem.compliance.validators.quality_mypy_validator.subprocess.run",
        return_value=fake_process,
    ):
        run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.ERROR
    assert run_result.evidence == ()


def test_error_when_mypy_output_is_unparseable(tmp_path: Path) -> None:
    """ERROR when MyPy's stdout is not valid JSON lines."""

    (tmp_path / "module.py").write_text("x: int = 1\n", encoding="utf-8")

    context = make_context(tmp_path, manifest={})
    validator = QualityMypyValidator()

    fake_process = subprocess.CompletedProcess(
        args=["mypy"],
        returncode=1,
        stdout="not json\n",
        stderr="",
    )

    with patch(
        "familyos_cli.plugins.ecosystem.compliance.validators.quality_mypy_validator.subprocess.run",
        return_value=fake_process,
    ):
        run_result = validator.validate(context)

    assert run_result.status is ValidatorStatus.ERROR
    assert run_result.evidence == ()
