"""Quality adapter for deterministic Documentation Framework validation."""

from __future__ import annotations

import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityRule,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.infrastructure.documentation import DocumentationValidator

_DOCUMENTATION = QualityEvidenceType("DOCUMENTATION")


class DocumentationQualityExecutor(QualityExecutorPort):
    """Normalize Documentation Framework validation into Quality results."""

    def __init__(
        self,
        *,
        finding_id_factory: Callable[[], QualityFindingId],
        evidence_id_factory: Callable[[], QualityEvidenceId],
        clock: Callable[[], datetime] | None = None,
        monotonic_clock: Callable[[], float] = time.monotonic,
        validator: DocumentationValidator | None = None,
    ) -> None:
        self._finding_id_factory = finding_id_factory
        self._evidence_id_factory = evidence_id_factory
        self._clock = clock or (lambda: datetime.now(UTC))
        self._monotonic_clock = monotonic_clock
        self._validator = validator or DocumentationValidator()

    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        started = self._monotonic_clock()
        if target.path is None:
            return QualityCheckResult(
                check_id=check_id,
                status=QualityStatus.ERROR,
                duration_seconds=max(0.0, self._monotonic_clock() - started),
                diagnostics=("Documentation quality target.path is required.",),
            )

        root = Path(target.path)
        if not root.exists() or not root.is_dir():
            return QualityCheckResult(
                check_id=check_id,
                status=QualityStatus.ERROR,
                duration_seconds=max(0.0, self._monotonic_clock() - started),
                diagnostics=(
                    f"Documentation quality target is not an accessible directory: {target.path}",
                ),
            )

        evidence_id = self._evidence_id_factory()
        try:
            validation = self._validator.validate(root)
        except Exception as exc:
            evidence = self._evidence(
                evidence_id=evidence_id,
                rule=rule,
                target=target,
                result=QualityEvidenceResult.ERROR,
                violation_count=0,
            )
            return QualityCheckResult(
                check_id=check_id,
                status=QualityStatus.ERROR,
                evidence=(evidence,),
                duration_seconds=max(0.0, self._monotonic_clock() - started),
                diagnostics=(f"Documentation validation could not complete: {exc}",),
            )

        status = (
            QualityStatus.FAIL
            if validation.violations
            else QualityStatus.PASS
        )
        evidence_result = (
            QualityEvidenceResult.FAIL
            if validation.violations
            else QualityEvidenceResult.PASS
        )
        evidence = self._evidence(
            evidence_id=evidence_id,
            rule=rule,
            target=target,
            result=evidence_result,
            violation_count=len(validation.violations),
        )
        findings = tuple(
            QualityFinding(
                id=self._finding_id_factory(),
                rule_id=rule.id,
                domain=rule.domain,
                severity=rule.severity,
                status=QualityStatus.FAIL,
                message=violation.message,
                target=target,
                location=violation.location,
                evidence_ids=(str(evidence_id),),
            )
            for violation in validation.violations
        )
        return QualityCheckResult(
            check_id=check_id,
            status=status,
            findings=findings,
            evidence=(evidence,),
            duration_seconds=max(0.0, self._monotonic_clock() - started),
        )

    def _evidence(
        self,
        *,
        evidence_id: QualityEvidenceId,
        rule: QualityRule,
        target: QualityTarget,
        result: QualityEvidenceResult,
        violation_count: int,
    ) -> QualityEvidence:
        return QualityEvidence(
            id=evidence_id,
            type=_DOCUMENTATION,
            source="quality.documentation",
            target=target,
            result=result,
            created_at=self._clock(),
            revision=target.revision,
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            tool="familyos-documentation-validator",
            metadata=(("violations", str(violation_count)),),
        )
