"""Profile-aware orchestration for canonical Quality assessments."""

from datetime import datetime

from familyos_cli.application.quality.quality_assessment_service import (
    QualityAssessmentService,
)
from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.application.quality.quality_profile_resolver import (
    QualityProfileResolver,
)
from familyos_cli.domain.quality import (
    QualityAssessment,
    QualityAssessmentId,
    QualityFindingId,
    QualityTarget,
)


class QualityProfileAssessmentService:
    """Resolve a governed profile and delegate canonical assessment aggregation."""

    def __init__(
        self,
        profile_resolver: QualityProfileResolver,
        assessment_service: QualityAssessmentService | None = None,
    ) -> None:
        if not isinstance(profile_resolver, QualityProfileResolver):
            raise TypeError("profile_resolver must be a QualityProfileResolver")
        if assessment_service is not None and not isinstance(
            assessment_service, QualityAssessmentService
        ):
            raise TypeError("assessment_service must be a QualityAssessmentService")
        self._profile_resolver = profile_resolver
        self._assessment_service = assessment_service or QualityAssessmentService()

    def assess(
        self,
        *,
        assessment_id: QualityAssessmentId,
        target: QualityTarget,
        check_results: tuple[QualityCheckResult, ...],
        blocking_finding_ids: tuple[QualityFindingId, ...],
        created_at: datetime,
    ) -> QualityAssessment:
        """Resolve the applicable profile and delegate Phase 10 aggregation."""
        profile = self._profile_resolver.resolve(target)
        return self._assessment_service.assess(
            assessment_id=assessment_id,
            target=target,
            profile=profile.reference,
            required_check_ids=profile.required_checks,
            check_results=check_results,
            blocking_finding_ids=blocking_finding_ids,
            created_at=created_at,
        )
