import json
from dataclasses import replace
from datetime import UTC, datetime

import pytest

from familyos_cli.domain.quality import (
    GateDecision,
    QualityAssessmentId,
    QualityCheckId,
    QualityEvidenceId,
    QualityFindingId,
    QualityGate,
    QualityGateCondition,
    QualityGateId,
    QualityRuleId,
    QualityTarget,
)
from familyos_cli.interfaces.cli.rendering.quality_gate_json import render_gate_json
from scripts.quality_ci_report import render_summary


def _gate() -> QualityGate:
    return QualityGate(
        id=QualityGateId("QLT-GATE-MERGE-001"),
        target=QualityTarget(
            "repository",
            "café",
            revision="abc",
            metadata=(("key", "one"), ("key", "two")),
        ),
        revision="abc",
        policy="QLT-GATE-MERGE-001@1.0.0",
        assessment_id=QualityAssessmentId("QLT-ASMT-X"),
        decision=GateDecision.FAIL,
        blocking_conditions=(
            QualityGateCondition(
                "check_not_accepted",
                "</pre><script>failed</script>",
                QualityCheckId("QLT-CHECK-X"),
                (QualityFindingId("QLT-FIND-X"),),
                (QualityRuleId("QLT-RULE-X"),),
                (QualityEvidenceId("QLT-EVID-X"),),
            ),
        ),
        evaluated_at=datetime(2026, 9, 3, tzinfo=UTC),
    )


def test_versioned_gate_json_preserves_canonical_fields_and_references() -> None:
    rendered = render_gate_json(_gate())
    data = json.loads(rendered)
    assert data["schema_version"] == "1.0.0" and rendered.endswith("\n")
    gate = data["gate"]
    assert set(gate) == {
        "id",
        "target",
        "revision",
        "policy",
        "assessment_id",
        "decision",
        "mode",
        "prevents_progression",
        "blocking_conditions",
        "evaluated_at",
    }
    assert gate["target"] == {
        "target_type": "repository",
        "identifier": "café",
        "revision": "abc",
        "version": None,
        "path": None,
        "metadata": [["key", "one"], ["key", "two"]],
    }
    assert gate["mode"] == "OBSERVE" and gate["prevents_progression"] is False
    assert gate["decision"] == "FAIL" and gate["revision"] == "abc"
    assert gate["assessment_id"] == "QLT-ASMT-X"
    assert gate["blocking_conditions"][0] == {
        "code": "check_not_accepted",
        "message": "</pre><script>failed</script>",
        "check_id": "QLT-CHECK-X",
        "finding_ids": ["QLT-FIND-X"],
        "rule_ids": ["QLT-RULE-X"],
        "evidence_ids": ["QLT-EVID-X"],
    }
    assert gate["evaluated_at"] == "2026-09-03T00:00:00+00:00"


def test_missing_assessment_and_check_are_explicit_nulls() -> None:
    gate = replace(
        _gate(),
        assessment_id=None,
        decision=GateDecision.ERROR,
        blocking_conditions=(QualityGateCondition("missing", "No assessment"),),
    )
    payload = json.loads(render_gate_json(gate))["gate"]
    assert payload["assessment_id"] is None
    assert payload["blocking_conditions"][0]["check_id"] is None


def test_invalid_utf8_fails_before_output() -> None:
    gate = replace(_gate(), policy="bad\ud800")
    with pytest.raises(UnicodeEncodeError):
        render_gate_json(gate)


def test_gate_summary_is_bounded_and_cannot_inject_html() -> None:
    gate = _gate()
    summary = render_summary(
        None,
        revision="abc",
        cli_exit_code=2,
        adapter_exit_code=2,
        adapter_error=None,
        gate=gate,
    )
    assert "would-fail" in summary and "OBSERVE" in summary
    assert "&lt;script&gt;" in summary and "<script>" not in summary
    assert (
        "QLT-FIND-X" in summary and "QLT-RULE-X" in summary and "QLT-EVID-X" in summary
    )
    huge = replace(
        gate, blocking_conditions=(QualityGateCondition("large", "x" * 100_000),)
    )
    summary = render_summary(
        None,
        revision="abc",
        cli_exit_code=2,
        adapter_exit_code=2,
        adapter_error=None,
        gate=huge,
    )
    assert len(summary) < 41_000
    assert "would-fail" in summary and "truncated" in summary
    assert "gate-observation.json" in summary
