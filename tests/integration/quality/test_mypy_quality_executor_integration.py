from __future__ import annotations

from datetime import UTC, datetime
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
from familyos_cli.infrastructure.quality import MypyQualityExecutor


def _rule() -> QualityRule:
    return QualityRule(
        id=QualityRuleId("QLT-RULE-MYPY-INTEGRATION"),
        requirement_id=None,
        domain=QualityDomain("QLT-DOM-QLT"),
        severity=QualitySeverity.HIGH,
        description="MyPy integration fixture must satisfy governed type policy",
        executor="mypy",
    )


def _executor() -> MypyQualityExecutor:
    finding_counter = iter(range(1, 20))
    evidence_counter = iter(range(1, 20))
    return MypyQualityExecutor(
        finding_id_factory=lambda: QualityFindingId(
            f"QLT-FIND-MYPY-INT-{next(finding_counter):03d}"
        ),
        evidence_id_factory=lambda: QualityEvidenceId(
            f"QLT-EVID-MYPY-INT-{next(evidence_counter):03d}"
        ),
        clock=lambda: datetime(2026, 9, 1, 12, 0, tzinfo=UTC),
    )


def _target(path: Path) -> QualityTarget:
    return QualityTarget(
        target_type="repository",
        identifier="mypy-integration-fixture",
        path=str(path),
    )


def test_real_mypy_valid_fixture_produces_normalized_pass(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "valid"
    fixture.mkdir()

    (fixture / "example.py").write_text(
        "def answer() -> int:\n"
        "    return 42\n",
        encoding="utf-8",
    )

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY-VALID"),
        rule=_rule(),
        target=_target(fixture),
    )

    assert result.status is QualityStatus.PASS
    assert result.findings == ()
    assert len(result.evidence) == 1

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.PASS
    assert evidence.type.value == "TYPE_VERIFICATION"
    assert evidence.source == "quality.mypy"
    assert evidence.tool == "mypy"
    assert evidence.tool_version is not None
    assert evidence.tool_version.startswith("mypy ")
    assert ("exit_code", "0") in evidence.metadata
    assert ("diagnostic_count", "0") in evidence.metadata
    assert ("mypy_codes", "[]") in evidence.metadata
    assert result.duration_seconds >= 0.0


def test_real_mypy_invalid_fixture_produces_structured_finding(
    tmp_path: Path,
) -> None:
    fixture = tmp_path / "invalid"
    fixture.mkdir()

    invalid_file = fixture / "example.py"
    invalid_file.write_text(
        "def answer() -> int:\n"
        '    return "wrong"\n',
        encoding="utf-8",
    )

    rule = _rule()
    target = _target(fixture)

    result = _executor().execute(
        check_id=QualityCheckId("QLT-CHECK-MYPY-INVALID"),
        rule=rule,
        target=target,
    )

    assert result.status is QualityStatus.FAIL
    assert len(result.findings) == 1
    assert len(result.evidence) == 1

    finding = result.findings[0]
    assert finding.rule_id == rule.id
    assert finding.domain == rule.domain
    assert finding.severity == rule.severity
    assert finding.status is QualityStatus.FAIL
    assert finding.message == (
        'Incompatible return value type (got "str", expected "int")'
    )
    assert finding.location is not None
    assert finding.location.endswith("example.py:2:11")
    assert finding.target == target
    assert finding.evidence_ids == ("QLT-EVID-MYPY-INT-001",)

    evidence = result.evidence[0]
    assert evidence.result is QualityEvidenceResult.FAIL
    assert evidence.type.value == "TYPE_VERIFICATION"
    assert evidence.source == "quality.mypy"
    assert evidence.tool == "mypy"
    assert evidence.tool_version is not None
    assert evidence.tool_version.startswith("mypy ")
    assert ("exit_code", "1") in evidence.metadata
    assert ("diagnostic_count", "1") in evidence.metadata
    assert ("mypy_codes", '["return-value"]') in evidence.metadata
    assert result.duration_seconds >= 0.0
