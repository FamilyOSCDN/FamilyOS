from __future__ import annotations

from datetime import UTC, datetime
from itertools import count
from pathlib import Path

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
        id=QualityRuleId("QLT-RULE-PYTEST-INTEGRATION"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-QLT"),
        severity=QualitySeverity.HIGH,
        description="Real Pytest integration must pass",
        executor="pytest",
    )


def _executor() -> PytestQualityExecutor:
    finding_ids = count(1)
    evidence_ids = count(1)
    return PytestQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-PYTEST-INT-{next(finding_ids):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-PYTEST-INT-{next(evidence_ids):03d}"
        ),
        clock=lambda: datetime(2026, 9, 1, 20, 0, tzinfo=UTC),
    )


def _target(path: Path) -> QualityTarget:
    return QualityTarget(
        target_type="repository",
        identifier="pytest-integration-fixture",
        path=str(path),
    )


def test_real_pytest_pass_execution_produces_canonical_test_evidence(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_real_pass.py"
    test_file.write_text(
        "def test_real_pass() -> None:\n"
        "    assert 2 + 2 == 4\n",
        encoding="utf-8",
    )

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST-INTEGRATION-PASS"),
        rule=_rule(),
        target=_target(test_file),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1

    evidence = result.evidence[0]
    assert evidence.type.value == "TEST"
    assert evidence.source == "quality.pytest"
    assert evidence.tool == "pytest"
    assert evidence.tool_version is not None
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.revision is None

    metadata = dict(evidence.metadata)
    assert metadata["exit_code"] == "0"
    assert metadata["passed"] == "1"
    assert metadata["failed"] == "0"
    assert metadata["errors"] == "0"


def test_real_pytest_assertion_failure_produces_fail_finding_and_evidence(
    tmp_path: Path,
) -> None:
    test_file = tmp_path / "test_real_fail.py"
    test_file.write_text(
        "def test_real_fail() -> None:\n"
        "    assert 2 + 2 == 5\n",
        encoding="utf-8",
    )

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-PYTEST-INTEGRATION-FAIL"),
        rule=_rule(),
        target=_target(test_file),
    )

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 1
    assert len(result.evidence) == 1

    finding = result.findings[0]
    assert finding.status is QualityStatus.FAIL
    assert finding.rule_id == _rule().id
    assert finding.domain == _rule().domain
    assert finding.severity == _rule().severity
    assert finding.target.path == str(test_file)
    assert finding.evidence_ids == ("QLT-EVID-PYTEST-INT-001",)

    evidence = result.evidence[0]
    assert evidence.type.value == "TEST"
    assert evidence.source == "quality.pytest"
    assert evidence.tool == "pytest"
    assert evidence.result is QualityEvidenceResult.FAIL

    metadata = dict(evidence.metadata)
    assert metadata["exit_code"] == "1"
    assert metadata["passed"] == "0"
    assert metadata["failed"] == "1"
    assert metadata["errors"] == "0"
