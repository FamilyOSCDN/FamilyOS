"""Public schema and byte-level serialization contracts for Quality reports."""

import json
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from familyos_cli.application.quality import (
    QualityAssessmentExecutionResult,
    QualityCheckResult,
)
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityDomain,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityRequirementId,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.interfaces.cli.rendering.quality_report_json import (
    QualityReportJsonRenderer,
)


@pytest.fixture
def execution() -> QualityAssessmentExecutionResult:
    target = QualityTarget(
        target_type="documentation", identifier="EPIC-TEST", revision="abc123",
        version="1.2.3", path="docs/test", metadata=(("owner", "équipe"), ("owner", "second")),
    )
    now = datetime(2026, 9, 3, 12, 0, tzinfo=UTC)
    evidence = QualityEvidence(
        id=QualityEvidenceId("QLT-EVID-Z"), type=QualityEvidenceType("DOCUMENTATION"),
        source="quality.documentation", target=target, result=QualityEvidenceResult.FAIL,
        created_at=now, revision=target.revision, rule_id=QualityRuleId("QLT-RULE-DOC-001"),
        requirement_id=QualityRequirementId("QLT-REQ-DOC"), tool="validator",
        tool_version="1", metadata=(("count", "1"), ("count", "2")), artifact="logs/doc.txt",
    )
    finding = QualityFinding(
        id=QualityFindingId("QLT-FIND-Z"), rule_id=QualityRuleId("QLT-RULE-DOC-001"),
        domain=QualityDomain("QLT-DOM-DOC"), severity=QualitySeverity.HIGH,
        status=QualityStatus.FAIL, message='Échec "titre"\n\t\x1b[31m', target=target,
        location="README.md:2", evidence_ids=("QLT-EVID-Z", "QLT-EVID-Z"),
    )
    check = QualityCheckResult(
        check_id=QualityCheckId("QLT-CHECK-DOC"), status=QualityStatus.FAIL,
        findings=(finding, finding), evidence=(evidence, evidence), duration_seconds=1.25,
        diagnostics=("échec", "échec"),
    )
    assessment = QualityAssessment(
        id=QualityAssessmentId("QLT-ASMT-TEST"), target=target, revision=target.revision,
        profile="QLT-PROFILE-DOCUMENTATION@1.0.0", status=QualityStatus.UNKNOWN,
        quality_state=QualityAssessmentState.UNKNOWN, evidence_ids=(evidence.id, evidence.id),
        finding_ids=(finding.id,), created_at=now,
    )
    return QualityAssessmentExecutionResult(assessment, (check,))


def test_version_one_payload_has_exact_fields_values_and_deterministic_bytes(
    execution: QualityAssessmentExecutionResult,
) -> None:
    target = {
        "target_type": "documentation", "identifier": "EPIC-TEST", "revision": "abc123",
        "version": "1.2.3", "path": "docs/test",
        "metadata": [["owner", "équipe"], ["owner", "second"]],
    }
    finding = {
        "id": "QLT-FIND-Z", "rule_id": "QLT-RULE-DOC-001", "domain": "QLT-DOM-DOC",
        "severity": "HIGH", "status": "FAIL", "message": 'Échec "titre"\n\t\x1b[31m',
        "target": target, "location": "README.md:2", "evidence_ids": ["QLT-EVID-Z", "QLT-EVID-Z"],
    }
    evidence = {
        "id": "QLT-EVID-Z", "type": "DOCUMENTATION", "source": "quality.documentation",
        "target": target, "result": "FAIL", "created_at": "2026-09-03T12:00:00+00:00",
        "revision": "abc123", "rule_id": "QLT-RULE-DOC-001", "requirement_id": "QLT-REQ-DOC",
        "tool": "validator", "tool_version": "1", "metadata": [["count", "1"], ["count", "2"]],
        "artifact": "logs/doc.txt",
    }
    expected = {
        "schema_version": "1.0.0",
        "assessment": {
            "id": "QLT-ASMT-TEST", "target": target, "revision": "abc123",
            "profile": "QLT-PROFILE-DOCUMENTATION@1.0.0", "status": "UNKNOWN",
            "quality_state": "UNKNOWN", "evidence_ids": ["QLT-EVID-Z", "QLT-EVID-Z"],
            "finding_ids": ["QLT-FIND-Z"], "created_at": "2026-09-03T12:00:00+00:00",
        },
        "check_results": [{
            "check_id": "QLT-CHECK-DOC", "status": "FAIL", "findings": [finding, finding],
            "evidence": [evidence, evidence], "duration_seconds": 1.25,
            "diagnostics": ["échec", "échec"],
        }],
    }
    renderer = QualityReportJsonRenderer()

    rendered = renderer.render(execution)

    assert json.loads(rendered) == expected
    assert rendered == json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
    assert rendered == renderer.render(execution)
    assert "\x1b" not in rendered
    assert "Échec" in rendered
    assert not rendered.encode("utf-8").startswith(b"\xef\xbb\xbf")


def test_absent_scalars_and_empty_collections_are_explicit(
    execution: QualityAssessmentExecutionResult,
) -> None:
    target = QualityTarget(target_type="documentation", identifier="test")
    check = execution.check_results[0]
    evidence = replace(
        check.evidence[0], target=target, revision=None, rule_id=None,
        requirement_id=None, tool=None, tool_version=None, metadata=(), artifact=None,
    )
    finding = replace(check.findings[0], target=target, location=None, evidence_ids=())
    output = replace(
        execution,
        assessment=replace(execution.assessment, target=target, revision=None, evidence_ids=(), finding_ids=()),
        check_results=(replace(check, findings=(finding,), evidence=(evidence,), diagnostics=()),),
    )

    payload = json.loads(QualityReportJsonRenderer().render(output))

    assert payload["assessment"]["target"] == {
        "target_type": "documentation", "identifier": "test", "revision": None,
        "version": None, "path": None, "metadata": [],
    }
    assert payload["assessment"]["evidence_ids"] == payload["assessment"]["finding_ids"] == []
    record = payload["check_results"][0]
    assert record["findings"][0]["location"] is None
    assert record["findings"][0]["evidence_ids"] == []
    assert record["diagnostics"] == []
    for key in ("revision", "rule_id", "requirement_id", "tool", "tool_version", "artifact"):
        assert record["evidence"][0][key] is None
    empty = json.loads(QualityReportJsonRenderer().render(replace(output, check_results=())))
    assert empty["check_results"] == []


@pytest.mark.parametrize("duration", (float("nan"), float("inf")))
def test_nonfinite_numbers_cannot_be_emitted(
    execution: QualityAssessmentExecutionResult, duration: float,
) -> None:
    output = replace(execution, check_results=(replace(execution.check_results[0], duration_seconds=duration),))
    with pytest.raises(ValueError, match="Out of range float"):
        QualityReportJsonRenderer().render(output)


def test_invalid_utf8_string_is_rejected(execution: QualityAssessmentExecutionResult) -> None:
    output = replace(execution, check_results=(replace(execution.check_results[0], diagnostics=("\ud800",)),))
    with pytest.raises(UnicodeError):
        QualityReportJsonRenderer().render(output)
