"""Versioned, deterministic JSON adapter for retained Quality execution output."""

import json

from familyos_cli.application.quality import (
    QualityAssessmentExecutionResult,
    QualityCheckResult,
)
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityEvidence,
    QualityFinding,
    QualityTarget,
)


class QualityReportJsonRenderer:
    """Serialize the public Quality report 1.0.0 schema without reassessment."""

    def render(self, result: QualityAssessmentExecutionResult) -> str:
        """Build a complete UTF-8-compatible JSON document before output."""
        payload = {
            "schema_version": "1.0.0",
            "assessment": self._assessment(result.assessment),
            "check_results": [self._check(check) for check in result.check_results],
        }
        rendered = json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        rendered.encode("utf-8")
        return rendered

    @staticmethod
    def _target(target: QualityTarget) -> dict[str, object]:
        return {
            "target_type": target.target_type,
            "identifier": target.identifier,
            "revision": target.revision,
            "version": target.version,
            "path": target.path,
            "metadata": [list(entry) for entry in target.metadata],
        }

    def _assessment(self, assessment: QualityAssessment) -> dict[str, object]:
        return {
            "id": str(assessment.id),
            "target": self._target(assessment.target),
            "revision": assessment.revision,
            "profile": assessment.profile,
            "status": assessment.status.value,
            "quality_state": assessment.quality_state.value,
            "evidence_ids": [str(value) for value in assessment.evidence_ids],
            "finding_ids": [str(value) for value in assessment.finding_ids],
            "created_at": assessment.created_at.isoformat(),
        }

    def _check(self, check: QualityCheckResult) -> dict[str, object]:
        return {
            "check_id": str(check.check_id),
            "status": check.status.value,
            "findings": [self._finding(finding) for finding in check.findings],
            "evidence": [self._evidence(evidence) for evidence in check.evidence],
            "duration_seconds": check.duration_seconds,
            "diagnostics": list(check.diagnostics),
        }

    def _finding(self, finding: QualityFinding) -> dict[str, object]:
        return {
            "id": str(finding.id),
            "rule_id": str(finding.rule_id),
            "domain": str(finding.domain),
            "severity": finding.severity.value,
            "status": finding.status.value,
            "message": finding.message,
            "target": self._target(finding.target),
            "location": finding.location,
            "evidence_ids": list(finding.evidence_ids),
        }

    def _evidence(self, evidence: QualityEvidence) -> dict[str, object]:
        return {
            "id": str(evidence.id),
            "type": str(evidence.type),
            "source": evidence.source,
            "target": self._target(evidence.target),
            "result": evidence.result.value,
            "created_at": evidence.created_at.isoformat(),
            "revision": evidence.revision,
            "rule_id": str(evidence.rule_id) if evidence.rule_id is not None else None,
            "requirement_id": (
                str(evidence.requirement_id) if evidence.requirement_id is not None else None
            ),
            "tool": evidence.tool,
            "tool_version": evidence.tool_version,
            "metadata": [list(entry) for entry in evidence.metadata],
            "artifact": evidence.artifact,
        }
