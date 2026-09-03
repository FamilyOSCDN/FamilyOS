"""Validate transported Quality evidence and render bounded CI feedback."""

import html
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

from familyos_cli.application.quality import (
    REPOSITORY_PROFILE,
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
    QualityGate,
    QualityRequirementId,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)


def _object(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ValueError("report value must be an object")
    return value


def _array(value: object) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError("report collection must be an array")
    return value


def _metadata(value: object) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for entry in _array(value):
        pair = _array(entry)
        if len(pair) != 2 or not all(isinstance(item, str) for item in pair):
            raise ValueError("report metadata must contain string pairs")
        pairs.append((pair[0], pair[1]))
    return tuple(pairs)


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("report timestamp must be a string")
    return datetime.fromisoformat(value)


def _target(value: object) -> QualityTarget:
    row = _object(value)
    return QualityTarget(
        target_type=row["target_type"], identifier=row["identifier"], revision=row["revision"],
        version=row["version"], path=row["path"], metadata=_metadata(row["metadata"]),
    )


def _finding(value: object) -> QualityFinding:
    row = _object(value)
    return QualityFinding(
        id=QualityFindingId(row["id"]), rule_id=QualityRuleId(row["rule_id"]),
        domain=QualityDomain(row["domain"]), severity=QualitySeverity(row["severity"]),
        status=QualityStatus(row["status"]), message=row["message"], target=_target(row["target"]),
        location=row["location"], evidence_ids=tuple(_array(row["evidence_ids"])),
    )


def _evidence(value: object) -> QualityEvidence:
    row = _object(value)
    return QualityEvidence(
        id=QualityEvidenceId(row["id"]), type=QualityEvidenceType(row["type"]),
        source=row["source"], target=_target(row["target"]), result=QualityEvidenceResult(row["result"]),
        created_at=_time(row["created_at"]), revision=row["revision"],
        rule_id=QualityRuleId(row["rule_id"]) if row["rule_id"] is not None else None,
        requirement_id=QualityRequirementId(row["requirement_id"]) if row["requirement_id"] is not None else None,
        tool=row["tool"], tool_version=row["tool_version"], metadata=_metadata(row["metadata"]), artifact=row["artifact"],
    )


def _check(value: object) -> QualityCheckResult:
    row = _object(value)
    result = QualityCheckResult(
        check_id=QualityCheckId(row["check_id"]), status=QualityStatus(row["status"]),
        findings=tuple(_finding(item) for item in _array(row["findings"])),
        evidence=tuple(_evidence(item) for item in _array(row["evidence"])),
        duration_seconds=row["duration_seconds"], diagnostics=tuple(_array(row["diagnostics"])),
    )
    if not math.isfinite(result.duration_seconds):
        raise ValueError("report duration must be finite")
    return result


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError(f"nonstandard JSON number: {value}")


def read_report(path: Path, target: QualityTarget) -> QualityAssessmentExecutionResult:
    """Accept a versioned report only for the checked repository execution."""
    payload = _object(json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object,
        parse_constant=_invalid_constant,
    ))
    if payload["schema_version"] != "1.0.0":
        raise ValueError("unsupported Quality report schema")
    row = _object(payload["assessment"])
    assessment = QualityAssessment(
        id=QualityAssessmentId(row["id"]), target=_target(row["target"]), revision=row["revision"],
        profile=row["profile"], status=QualityStatus(row["status"]),
        quality_state=QualityAssessmentState(row["quality_state"]),
        evidence_ids=tuple(QualityEvidenceId(item) for item in _array(row["evidence_ids"])),
        finding_ids=tuple(QualityFindingId(item) for item in _array(row["finding_ids"])),
        created_at=_time(row["created_at"]),
    )
    checks = tuple(_check(item) for item in _array(payload["check_results"]))
    if assessment.target != target or assessment.revision != target.revision:
        raise ValueError("report target/revision does not match checked source")
    if assessment.profile != REPOSITORY_PROFILE.reference:
        raise ValueError("report does not use the governed repository profile")
    if tuple(check.check_id for check in checks) != REPOSITORY_PROFILE.required_checks:
        raise ValueError("report required checks do not match governed profile order")
    findings = tuple(finding for check in checks for finding in check.findings)
    evidence = tuple(item for check in checks for item in check.evidence)
    if any(item.target != target for item in findings) or any(item.target != target for item in evidence):
        raise ValueError("report finding/evidence target does not match checked source")
    if any(item.revision is not None and item.revision != target.revision for item in evidence):
        raise ValueError("report evidence revision does not match checked source")
    evidence_ids = {item.id for item in evidence}
    if set(assessment.evidence_ids) != evidence_ids or set(assessment.finding_ids) != {item.id for item in findings}:
        raise ValueError("report assessment identifiers do not match retained details")
    if any(QualityEvidenceId(reference) not in evidence_ids for item in findings for reference in item.evidence_ids):
        raise ValueError("report finding refers to absent evidence")
    return QualityAssessmentExecutionResult(assessment, checks)


def render_summary(
    result: QualityAssessmentExecutionResult | None, *, revision: str | None,
    cli_exit_code: int | None, adapter_exit_code: int, adapter_error: str | None,
    gate: QualityGate | None = None,
) -> str:
    """Show operational and Quality outcomes without inferring gate policy."""
    lines = [
        f"Checked revision: {revision or 'unavailable'}",
        f"CLI exit code: {cli_exit_code if cli_exit_code is not None else 'not completed'}",
        f"Adapter exit code: {adapter_exit_code}",
    ]
    if adapter_error is not None:
        lines.append(f"Adapter error: {adapter_error}")
    if gate is not None:
        label = {"PASS": "would-pass", "FAIL": "would-fail", "ERROR": "evaluation-error"}[gate.decision.value]
        lines.extend((f"Gate policy: {gate.policy}", f"Gate mode: {gate.mode}; decision: {label}; prevents progression: false"))
        for condition in gate.blocking_conditions[:100]:
            lines.extend((
                f"  {condition.code}: {condition.message}",
                f"    Check: {condition.check_id or 'assessment'}",
                f"    Findings: {', '.join(str(value) for value in condition.finding_ids[:100])}",
                f"    Rules: {', '.join(str(value) for value in condition.rule_ids[:100])}",
                f"    Evidence: {', '.join(str(value) for value in condition.evidence_ids[:100])}",
            ))
        lines.append("Full gate conditions and references: gate-observation.json.")
    if result is not None:
        assessment = result.assessment
        lines.extend((
            f"Profile: {assessment.profile}",
            f"Assessment: {assessment.status.value} / {assessment.quality_state.value}",
        ))
        for check in result.check_results:
            lines.append(f"{check.check_id}: {check.status.value}; findings: {len(check.findings)}")
            lines.extend(f"  Diagnostic: {message}" for message in check.diagnostics[:20])
            if len(check.diagnostics) > 20:
                lines.append("  Additional diagnostics are in quality-report.json.")
        findings = [finding for check in result.check_results for finding in check.findings]
        lines.append(f"Findings shown: {min(len(findings), 100)} / {len(findings)}")
        for finding in findings[:100]:
            lines.extend((
                f"{finding.id} | {finding.rule_id} | {finding.severity.value}",
                f"  Location: {finding.location or 'not supplied'}",
                f"  {finding.message}",
            ))
    body = "\n".join(lines)
    if len(body) > 40_000:
        body = body[:40_000] + "\n[Summary truncated; full details are in quality-report.json.]"
    return (
        "# Quality observation\n\n"
        "Observation only; merge and release progression are not blocked.\n\n"
        f"<pre>{html.escape(body)}</pre>\n\n"
        "Full evidence: quality-report.json, stdout.log, stderr.log, execution.json, gate-observation.json "
        "in the familyos-quality-observation artifact.\n"
    )
