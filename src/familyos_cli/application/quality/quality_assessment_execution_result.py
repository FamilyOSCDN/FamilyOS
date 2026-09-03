"""Application output retaining one Quality execution and its assessment."""

from dataclasses import dataclass

from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.domain.quality import QualityAssessment


@dataclass(frozen=True, slots=True)
class QualityAssessmentExecutionResult:
    """Retain canonical objects; orchestration owns their assessment correlation."""

    assessment: QualityAssessment
    check_results: tuple[QualityCheckResult, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.assessment, QualityAssessment):
            raise TypeError(
                "QualityAssessmentExecutionResult assessment must be a QualityAssessment"
            )
        if not isinstance(self.check_results, tuple):
            raise TypeError(
                "QualityAssessmentExecutionResult check_results must be a tuple"
            )
        if not all(
            isinstance(result, QualityCheckResult) for result in self.check_results
        ):
            raise TypeError(
                "QualityAssessmentExecutionResult check_results must contain "
                "QualityCheckResult values"
            )
