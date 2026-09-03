from datetime import UTC, datetime

import pytest

from familyos_cli.application.ports.quality.quality_executor import (
    QualityExecutorPort,
)
from familyos_cli.application.quality import (
    QualityProfileAssessmentService,
    QualityProfileRegistry,
    QualityProfileResolver,
)
from familyos_cli.application.quality.quality_assessment_execution_service import (
    QualityAssessmentExecutionService,
)
from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.application.quality.quality_execution_binding import (
    QualityExecutionBinding,
)
from familyos_cli.application.quality.quality_execution_service import (
    QualityExecutionService,
)
from familyos_cli.domain.quality import (
    QualityAssessmentId,
    QualityAssessmentState,
    QualityCheckId,
    QualityDomain,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityProfile,
    QualityProfileId,
    QualityRule,
    QualityRuleId,
    QualitySeverity,
    QualityStatus,
    QualityTarget,
)

NOW = datetime(2026, 9, 3, 9, 0, tzinfo=UTC)
TARGET = QualityTarget(
    target_type="repository",
    identifier="familyos-cli",
    revision="abc123",
    path=".",
)
CHECK = QualityCheckId("QLT-CHECK-RUFF")
RULE = QualityRule(
    id=QualityRuleId("QLT-RULE-STA-001"),
    requirement_id=None,
    domain=QualityDomain("QLT-DOM-MNT"),
    severity=QualitySeverity.MEDIUM,
    description="Ruff must pass.",
)


class Executor(QualityExecutorPort):
    def __init__(self, status: QualityStatus = QualityStatus.PASS) -> None:
        self.status = status
        self.calls: list[tuple[QualityCheckId, QualityRule, QualityTarget]] = []

    def execute(
        self,
        *,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
    ) -> QualityCheckResult:
        self.calls.append((check_id, rule, target))
        evidence_result = (
            QualityEvidenceResult.PASS
            if self.status is QualityStatus.PASS
            else QualityEvidenceResult.FAIL
        )
        evidence = QualityEvidence(
            id=QualityEvidenceId("QLT-EVID-TEST"),
            type=QualityEvidenceType("TEST"),
            source="test",
            target=target,
            result=evidence_result,
            created_at=NOW,
            revision=target.revision,
        )
        return QualityCheckResult(
            check_id=check_id,
            status=self.status,
            evidence=(evidence,),
        )


def make_service(
    status: QualityStatus = QualityStatus.PASS,
) -> tuple[QualityAssessmentExecutionService, Executor]:
    registry = QualityProfileRegistry()
    registry.register(
        QualityProfile(
            id=QualityProfileId("QLT-PROFILE-REPOSITORY"),
            version="1",
            target_types=("repository",),
            required_checks=(CHECK,),
            required_domains=(QualityDomain("QLT-DOM-MNT"),),
            severity_policy=(),
        )
    )
    resolver = QualityProfileResolver(registry)
    executor = Executor(status)
    execution = QualityExecutionService(
        resolver,
        (QualityExecutionBinding(CHECK, RULE, executor),),
    )
    service = QualityAssessmentExecutionService(
        execution_service=execution,
        assessment_service=QualityProfileAssessmentService(resolver),
        assessment_id_factory=lambda: QualityAssessmentId("QLT-ASMT-TEST"),
        clock=lambda: NOW,
    )
    return service, executor


def test_execute_produces_canonical_assessment() -> None:
    service, executor = make_service()

    assessment = service.execute(TARGET)

    assert executor.calls == [(CHECK, RULE, TARGET)]
    assert assessment.id == QualityAssessmentId("QLT-ASMT-TEST")
    assert assessment.profile == "QLT-PROFILE-REPOSITORY@1"
    assert assessment.status is QualityStatus.PASS
    assert assessment.quality_state is QualityAssessmentState.PASS
    assert assessment.created_at == NOW


def test_fail_is_not_implicitly_blocking() -> None:
    service, _ = make_service(QualityStatus.FAIL)

    assessment = service.execute(TARGET)

    assert assessment.status is QualityStatus.UNKNOWN
    assert assessment.quality_state is QualityAssessmentState.UNKNOWN


def test_rejects_invalid_target_before_execution() -> None:
    service, executor = make_service()

    with pytest.raises(TypeError, match="target must be a QualityTarget"):
        service.execute(object())  # type: ignore[arg-type]

    assert executor.calls == []
