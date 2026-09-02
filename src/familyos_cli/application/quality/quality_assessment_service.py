from datetime import datetime

from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityFindingId,
    QualityStatus,
    QualityTarget,
)


class QualityAssessmentService:
    def assess(
        self,
        *,
        assessment_id: QualityAssessmentId,
        target: QualityTarget,
        profile: str,
        required_check_ids: tuple[QualityCheckId, ...],
        check_results: tuple[QualityCheckResult, ...],
        blocking_finding_ids: tuple[QualityFindingId, ...],
        created_at: datetime,
    ) -> QualityAssessment:
        check_ids = tuple(result.check_id for result in check_results)
        if len(set(check_ids)) != len(check_ids):
            raise ValueError(
                "QualityAssessment check_results must have unique check_ids"
            )

        by_check = {result.check_id: result for result in check_results}
        required = tuple(by_check.get(check_id) for check_id in required_check_ids)
        present = tuple(result for result in required if result is not None)

        evidence = tuple(
            evidence for result in check_results for evidence in result.evidence
        )
        findings = tuple(
            finding for result in check_results for finding in result.findings
        )

        if any(evidence.target != target for evidence in evidence):
            raise ValueError(
                "QualityAssessment evidence target must match assessment target"
            )
        if any(finding.target != target for finding in findings):
            raise ValueError(
                "QualityAssessment finding target must match assessment target"
            )
        if any(
            evidence.revision is not None and evidence.revision != target.revision
            for evidence in evidence
        ):
            raise ValueError(
                "QualityAssessment evidence revision must match assessment target revision"
            )

        evidence_ids = tuple(sorted({evidence.id for evidence in evidence}, key=str))
        finding_ids = tuple(sorted({finding.id for finding in findings}, key=str))

        missing = any(result is None for result in required)
        error = any(result.status is QualityStatus.ERROR for result in present)
        incomplete = any(
            result.status in (QualityStatus.SKIPPED, QualityStatus.UNKNOWN)
            for result in present
        )
        missing_evidence = any(not result.evidence for result in present)
        blocking = bool(set(finding_ids) & set(blocking_finding_ids))
        warning = any(
            result.status is QualityStatus.WARNING for result in present
        ) or any(
            f.status is QualityStatus.WARNING
            for result in present
            for f in result.findings
        )

        if error:
            status, state = QualityStatus.ERROR, QualityAssessmentState.UNKNOWN
        elif missing or incomplete or missing_evidence:
            status, state = QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN
        elif blocking:
            status, state = QualityStatus.FAIL, QualityAssessmentState.FAIL
        elif warning:
            status, state = (
                QualityStatus.WARNING,
                QualityAssessmentState.PASS_WITH_WARNINGS,
            )
        elif present and all(result.status is QualityStatus.PASS for result in present):
            status, state = QualityStatus.PASS, QualityAssessmentState.PASS
        else:
            status, state = QualityStatus.UNKNOWN, QualityAssessmentState.UNKNOWN

        return QualityAssessment(
            id=assessment_id,
            target=target,
            revision=target.revision,
            profile=profile,
            status=status,
            quality_state=state,
            evidence_ids=evidence_ids,
            finding_ids=finding_ids,
            created_at=created_at,
        )
