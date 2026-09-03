"""Acceptance and safe summary contracts for transported Quality results."""

import json
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from familyos_cli.domain.quality import QualityStatus, QualityTarget
from scripts.quality_ci_report import read_report, render_summary


def target(path: Path) -> QualityTarget:
    return QualityTarget(target_type="repository", identifier="familyos-cli", path=str(path), revision="abc123")


def test_report_is_reconstructed_without_reassessment(
    tmp_path: Path, ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    payload = ci_report_factory(tmp_path, "abc123")
    report = tmp_path / "report.json"
    report.write_text(json.dumps(payload), encoding="utf-8")
    result = read_report(report, target(tmp_path))
    assert result.assessment.status is QualityStatus.PASS
    assert [str(check.check_id) for check in result.check_results] == [check["check_id"] for check in payload["check_results"]]


@pytest.mark.parametrize("change", [
    "schema", "profile", "target", "revision", "missing-check", "check-order",
    "evidence-target", "evidence-revision", "evidence-ids", "invalid-id", "status",
    "naive-time", "non-array", "missing-field", "duration",
])
def test_inconsistent_transport_is_rejected(
    tmp_path: Path, ci_report_factory: Callable[[Path, str], dict[str, Any]], change: str,
) -> None:
    payload = deepcopy(ci_report_factory(tmp_path, "abc123"))
    assessment, checks = payload["assessment"], payload["check_results"]
    if change == "schema":
        payload["schema_version"] = "2.0.0"
    elif change == "profile":
        assessment["profile"] = "QLT-PROFILE-OTHER@1.0.0"
    elif change == "target":
        assessment["target"] = {**assessment["target"], "identifier": "other"}
    elif change == "revision":
        assessment["revision"] = "stale"
    elif change == "missing-check":
        checks.pop()
    elif change == "check-order":
        checks.reverse()
    elif change == "evidence-target":
        checks[0]["evidence"][0]["target"] = {**assessment["target"], "identifier": "other"}
    elif change == "evidence-revision":
        checks[0]["evidence"][0]["revision"] = "stale"
    elif change == "evidence-ids":
        assessment["evidence_ids"] = []
    elif change == "invalid-id":
        assessment["id"] = "invalid"
    elif change == "status":
        checks[0]["status"] = "NOT_APPLICABLE"
    elif change == "naive-time":
        assessment["created_at"] = "2026-09-03T12:00:00"
    elif change == "non-array":
        checks[0]["diagnostics"] = "failure"
    elif change == "missing-field":
        del checks[0]["evidence"]
    else:
        checks[0]["duration_seconds"] = True
    report = tmp_path / "report.json"
    report.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises((TypeError, ValueError, KeyError)):
        read_report(report, target(tmp_path))


@pytest.mark.parametrize("value", ('{"a": 1, "a": 2}', '{"x": NaN}', '{"x": Infinity}', 'not JSON'))
def test_ambiguous_or_nonstandard_json_is_rejected(tmp_path: Path, value: str) -> None:
    report = tmp_path / "report.json"
    report.write_text(value, encoding="utf-8")
    with pytest.raises(ValueError):
        read_report(report, target(tmp_path))


def test_numeric_overflow_is_rejected(
    tmp_path: Path, ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    value = json.dumps(ci_report_factory(tmp_path, "abc123")).replace('"duration_seconds": 0.1', '"duration_seconds": 1e999')
    report = tmp_path / "report.json"
    report.write_text(value, encoding="utf-8")
    with pytest.raises(ValueError, match="finite"):
        read_report(report, target(tmp_path))


def test_normalized_error_without_evidence_remains_accepted(
    tmp_path: Path, ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    payload = ci_report_factory(tmp_path, "abc123")
    first = payload["check_results"][0]
    payload["assessment"]["evidence_ids"].remove(first["evidence"][0]["id"])
    first.update(status="ERROR", evidence=[], diagnostics=["executable missing"])
    payload["assessment"].update(status="ERROR", quality_state="UNKNOWN")
    report = tmp_path / "report.json"
    report.write_text(json.dumps(payload), encoding="utf-8")
    result = read_report(report, target(tmp_path))
    assert result.check_results[0].evidence == ()
    assert result.check_results[0].diagnostics == ("executable missing",)


def test_findings_are_correlated_and_summary_text_is_escaped_and_bounded(
    tmp_path: Path, ci_report_factory: Callable[[Path, str], dict[str, Any]],
) -> None:
    payload = ci_report_factory(tmp_path, "abc123")
    first = payload["check_results"][0]
    first["status"] = "FAIL"
    first["findings"] = [{
        "id": "QLT-FIND-TEST", "rule_id": "QLT-RULE-TEST", "domain": "QLT-DOM-DOC",
        "severity": "HIGH", "status": "FAIL", "message": '</pre><script>bad</script>\n' + "x" * 50_000,
        "target": payload["assessment"]["target"], "location": "README.md:9",
        "evidence_ids": [first["evidence"][0]["id"]],
    }] * 101
    payload["assessment"].update(status="UNKNOWN", quality_state="UNKNOWN", finding_ids=["QLT-FIND-TEST"])
    report = tmp_path / "report.json"
    report.write_text(json.dumps(payload), encoding="utf-8")
    result = read_report(report, target(tmp_path))

    summary = render_summary(result, revision="abc123", cli_exit_code=2, adapter_exit_code=2, adapter_error=None)

    assert "UNKNOWN / UNKNOWN" in summary
    assert "Findings shown: 100 / 101" in summary
    assert "QLT-RULE-TEST | HIGH" in summary and "README.md:9" in summary
    assert "<script>" not in summary and "&lt;script&gt;" in summary
    assert "Summary truncated" in summary
    assert len(summary.encode("utf-8")) < 1_048_576
    first["findings"][0]["evidence_ids"] = ["QLT-EVID-MISSING"]
    report.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="absent evidence"):
        read_report(report, target(tmp_path))
