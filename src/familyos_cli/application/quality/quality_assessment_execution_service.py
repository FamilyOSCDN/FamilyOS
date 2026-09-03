"""Application orchestration for governed Quality execution and assessment."""

from collections.abc import Callable
from datetime import datetime

from familyos_cli.application.quality.quality_execution_service import (
    QualityExecutionService,
)
from familyos_cli.application.quality.quality_profile_assessment_service import (
    QualityProfileAssessmentService,
)
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityTarget,
)


class QualityAssessmentExecutionService:
    """Execute governed checks and produce one canonical Quality assessment."""

    def __init__(
        self,
        execution_service: QualityExecutionService,
        assessment_service: QualityProfileAssessmentService,
        assessment_id_factory: Callable[[], QualityAssessmentId],
        clock: Callable[[], datetime],
    ) -> None:
        if not isinstance(execution_service, QualityExecutionService):
            raise TypeError("execution_service must be a QualityExecutionService")
        if not isinstance(assessment_service, QualityProfileAssessmentService):
            raise TypeError(
                "assessment_service must be a QualityProfileAssessmentService"
            )
        if not callable(assessment_id_factory):
            raise TypeError("assessment_id_factory must be callable")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._execution_service = execution_service
        self._assessment_service = assessment_service
        self._assessment_id_factory = assessment_id_factory
        self._clock = clock

    def execute(self, target: QualityTarget) -> QualityAssessment:
        if not isinstance(target, QualityTarget):
            raise TypeError("target must be a QualityTarget")
        results = self._execution_service.execute(target)
        return self._assessment_service.assess(
            assessment_id=self._assessment_id_factory(),
            target=target,
            check_results=results,
            blocking_finding_ids=(),
            created_at=self._clock(),
        )
